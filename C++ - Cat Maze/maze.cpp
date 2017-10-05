
//The headers
#include "SDL.h"        // `pkg-config --cflags sdl` `pkg-config --libs sdl`
#include "SDL_image.h"	// -lSDL_image
#include "SDL_ttf.h"	// -lSDL_ttf
#include "SDL_mixer.h"	// -lSDL_mixer
#include <string>
#include <fstream>
#include <cstdlib>
#include <sstream>
#include <string>


//Screen attributes
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int SCREEN_BPP = 32;

//The frame rate
const int FRAMES_PER_SECOND = 20;

//The cat dimensions
const int CAT_WIDTH = 50;
const int CAT_HEIGHT = 50;

//The dimensions of the level
const int LEVEL_WIDTH = 1280; // 80 X 16 = 1280
const int LEVEL_HEIGHT = 1040; // 80 X 13 = 960

//Tile constants
const int TILE_WIDTH = 80;
const int TILE_HEIGHT = 80;
const int TOTAL_TILES = 208; // 16 tiles X 13 tiles
const int TILE_SPRITES = 12;

//The different tile sprites
const int TILE_RED = 0;
const int TILE_GREEN = 1;
const int TILE_BLUE = 2;
const int TILE_CENTER = 3;
const int TILE_START = 5;
const int TILE_END = 7;

//Total sparkles
const int TOTAL_SPARKLES = 20;

//The surfaces
SDL_Surface *cat = NULL;
SDL_Surface *upCat = NULL;
SDL_Surface *downCat = NULL;
SDL_Surface *leftCat = NULL;

SDL_Surface *red = NULL;
SDL_Surface *green = NULL;
SDL_Surface *blue = NULL;
SDL_Surface *shimmer = NULL;
SDL_Surface *screen = NULL;
SDL_Surface *tileSheet = NULL;
SDL_Surface *seconds = NULL;
SDL_Surface *gameOver = NULL;

//Sprite from the tile sheet
SDL_Rect clips[ TILE_SPRITES ];

//The event structure
SDL_Event event;

//The camera
SDL_Rect camera = { 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT };

//Quit flag
bool quit = false;

// game over flag
bool game_over = false;
bool game_win = false;

//The font
TTF_Font *font = NULL;
TTF_Font *fontGA = NULL;

//The color of the font
SDL_Color textColor = { 255, 255, 0 };

//The music that will be played
Mix_Music *music = NULL;
//The music that will be played
Mix_Music *musicDeath = NULL;
// The ingame music
Mix_Music *musicIngame = NULL;


class Sparkle
{
    private:
    //Offsets
    int x, y;

    //Current frame of animation
    int frame;

    //Type of particle
    SDL_Surface *type;

    public:
    //Constructor
    Sparkle( int X, int Y );

    //Shows the particle
    void show();

    //Checks if particle is dead
    bool is_dead();
};

//The tile
class Tile
{
    private:
    //The attributes of the tile (offsets and dimensions of the tile and it also functions as a collision box)
    SDL_Rect box;

    //The tile type
    int type;

    public:
    //Initializes the variables
    Tile( int x, int y, int tileType ); // constructor (sets tile's offset)

    //Shows the tile
    void show();

    //Get the tile type
    int get_type();

    //Get the collision box
    SDL_Rect get_box();
};

//The cat
class Cat
{
    private:
    //The cat's collision box
    SDL_Rect box;

     //The sparkles
    Sparkle *sparkles[ TOTAL_SPARKLES ];

    public:
    //The velocity of the cat
    int xVel, yVel;

    //Initializes the variables
    Cat();

    //Cleans up sparkles
    ~Cat();

    //Takes key presses and adjusts the cat's velocity
    void handle_input();

    //Moves the cat
    void move( Tile *tiles[] );

    //Shows the sparkles
    void show_sparkles();

    //Shows the cat on the screen
    void show();

    //Sets the camera over the cat
    void set_camera();
};

//The timer
class Timer
{
    private:
    //The clock time when the timer started
    int startTicks;

    //The ticks stored when the timer was paused
    int pausedTicks;

    //The timer status
    bool paused;
    bool started;

    public:
    //Initializes variables
    Timer();

    //The various clock actions
    void start();
    void stop();
    void pause();
    void unpause();

    //Gets the timer's time
    int get_ticks();

    //Checks the status of the timer
    bool is_started();
    bool is_paused();
};

SDL_Surface *load_image( std::string filename )
{
    //The image that's loaded
    SDL_Surface* loadedImage = NULL;

    //The optimized surface that will be used
    SDL_Surface* optimizedImage = NULL;

    //Load the image
    loadedImage = IMG_Load( filename.c_str() );

    //If the image loaded
    if( loadedImage != NULL )
    {
        //Create an optimized surface
        optimizedImage = SDL_DisplayFormat( loadedImage );

        //Free the old surface
        SDL_FreeSurface( loadedImage );

        //If the surface was optimized
        if( optimizedImage != NULL )
        {
            //Color key surface
            SDL_SetColorKey( optimizedImage, SDL_SRCCOLORKEY, SDL_MapRGB( optimizedImage->format, 0, 255, 255 ) );
        }
    }

    //Return the optimized surface
    return optimizedImage;
}

void apply_surface( int x, int y, SDL_Surface* source, SDL_Surface* destination, SDL_Rect* clip = NULL )
{
    //Holds offsets
    SDL_Rect offset;

    //Get offsets
    offset.x = x;
    offset.y = y;

    //Blit
    SDL_BlitSurface( source, clip, destination, &offset );
}

bool check_collision( SDL_Rect A, SDL_Rect B )
{
    //The sides of the rectangles
    int leftA, leftB;
    int rightA, rightB;
    int topA, topB;
    int bottomA, bottomB;

    //Calculate the sides of rect A
    leftA = A.x;
    rightA = A.x + A.w;
    topA = A.y;
    bottomA = A.y + A.h;

    //Calculate the sides of rect B
    leftB = B.x;
    rightB = B.x + B.w;
    topB = B.y;
    bottomB = B.y + B.h;

    //If any of the sides from A are outside of B
    if( bottomA <= topB )
    {
        return false;
    }

    if( topA >= bottomB )
    {
        return false;
    }

    if( rightA <= leftB )
    {
        return false;
    }

    if( leftA >= rightB )
    {
        return false;
    }

    //If none of the sides from A are outside B
    return true;
}

bool init()
{
    //Initialize all SDL subsystems
    if( SDL_Init( SDL_INIT_EVERYTHING ) == -1 )
    {
        return false;
    }

    //Set up the screen
    screen = SDL_SetVideoMode( SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_BPP, SDL_SWSURFACE );

    //If there was an error in setting up the screen
    if( screen == NULL )
    {
        return false;
    }

    //Initialize SDL_ttf
    if( TTF_Init() == -1 )
    {
        return false;
    }


    //Initialize SDL_mixer
    if( Mix_OpenAudio( 22050, MIX_DEFAULT_FORMAT, 2, 4096 ) == -1 )
    {
        return false;
    }


    //Set the window caption
    SDL_WM_SetCaption( "  SEE HOW QUICKLY YOU CAN GET TO THE END OF THE MAZE!!", NULL );

    //Seed random
    srand( SDL_GetTicks() );


    //If everything initialized fine
    return true;
}

bool load_files()
{
    //Load the cat image
    cat = load_image( "catR.png" );
    upCat = load_image( "catU.png" );
    downCat = load_image( "catD.png" );
    leftCat = load_image( "catL.png" );

    //If there was a problem in loading the cat
    if( cat == NULL || upCat == NULL || downCat == NULL || leftCat == NULL)
    {
        return false;
    }

    //Load the tile sheet
    tileSheet = load_image( "tiles.png" );

    //Load the sparkles
    red = load_image( "red.bmp" );
    green = load_image( "green.bmp" );
    blue = load_image( "blue.bmp" );
    shimmer = load_image( "shimmer.bmp" );

    //If there was a problem in loading the tiles
    if( tileSheet == NULL )
    {
        return false;
    }

    //If there was a problem in loading the images
    if( ( shimmer == NULL ) || ( blue == NULL ) || ( green == NULL ) || ( red == NULL ) )
    {
        return false;
    }

    //Set alpha
    SDL_SetAlpha( red, SDL_SRCALPHA | SDL_RLEACCEL, 192 );
    SDL_SetAlpha( blue, SDL_SRCALPHA | SDL_RLEACCEL, 192 );
    SDL_SetAlpha( green, SDL_SRCALPHA | SDL_RLEACCEL, 192 );
    SDL_SetAlpha( shimmer, SDL_SRCALPHA | SDL_RLEACCEL, 192 );


    // Open the GAME OVER font
    fontGA = TTF_OpenFont( "lazy.ttf", 100 );

    // Open the timer font
    font = TTF_OpenFont( "lazy.ttf", 30 );


    //If there was an error in loading the font
    if( font == NULL || fontGA == NULL)
    {
        return false;
    }

    //Load the music
    music = Mix_LoadMUS( "fanfare.wav" );
    musicDeath = Mix_LoadMUS( "death.wav" );
    musicIngame = Mix_LoadMUS( "soda.wav" );

    //If there was a problem loading the music
    if( music == NULL || musicDeath == NULL)
    {
        return false;
    }


    //If everything loaded fine
    return true;
}


void clean_up( Tile *tiles[] )
{
    //Free the surfaces
    SDL_FreeSurface( cat );
    SDL_FreeSurface( upCat );
    SDL_FreeSurface( downCat );
    SDL_FreeSurface( leftCat );
    SDL_FreeSurface( red );
    SDL_FreeSurface( green );
    SDL_FreeSurface( blue );
    SDL_FreeSurface( shimmer );
    SDL_FreeSurface( cat );
    SDL_FreeSurface( tileSheet );
    SDL_FreeSurface( seconds );

    //Free the tiles
    for( int t = 0; t < TOTAL_TILES; t++ )
    {
        delete tiles[ t ];
    }

    //Close the font
    TTF_CloseFont( font );
    TTF_CloseFont( fontGA );

    //Quit SDL_ttf
    TTF_Quit();

    //Free the music
    Mix_FreeMusic( music );
    Mix_FreeMusic( musicDeath );
    Mix_FreeMusic( musicIngame );

    //Quit SDL_mixer
    Mix_CloseAudio();

    //Quit SDL
    SDL_Quit();
}

void clip_tiles()
{
    //Clip the sprite sheet
    clips[ TILE_RED ].x = 0;
    clips[ TILE_RED ].y = 0;
    clips[ TILE_RED ].w = TILE_WIDTH;
    clips[ TILE_RED ].h = TILE_HEIGHT;

    clips[ TILE_GREEN ].x = 0;
    clips[ TILE_GREEN ].y = 80;
    clips[ TILE_GREEN ].w = TILE_WIDTH;
    clips[ TILE_GREEN ].h = TILE_HEIGHT;

    clips[ TILE_BLUE ].x = 0;
    clips[ TILE_BLUE ].y = 160;
    clips[ TILE_BLUE ].w = TILE_WIDTH;
    clips[ TILE_BLUE ].h = TILE_HEIGHT;

    clips[ TILE_CENTER ].x = 160;
    clips[ TILE_CENTER ].y = 80;
    clips[ TILE_CENTER ].w = TILE_WIDTH;
    clips[ TILE_CENTER ].h = TILE_HEIGHT;

    clips[ TILE_START ].x = 240;
    clips[ TILE_START ].y = 0;
    clips[ TILE_START ].w = TILE_WIDTH;
    clips[ TILE_START ].h = TILE_HEIGHT;

    clips[ TILE_END ].x = 240;
    clips[ TILE_END ].y = 160;
    clips[ TILE_END ].w = TILE_WIDTH;
    clips[ TILE_END ].h = TILE_HEIGHT;
}

bool set_tiles( Tile *tiles[] )
{
    //The tile offsets
    int x = 0, y = 0;

    //Open the map
    std::ifstream map( "maze.map" );

    //If the map couldn't be loaded
    if( map.fail() )
    {
        return false;
    }

    //Initialize the tiles
    for( int t = 0; t < TOTAL_TILES; t++ )
    {
        //Determines what kind of tile will be made
        int tileType = -1;

        //Read tile from map file
        map >> tileType;

        //If the was a problem in reading the map
        if( map.fail() == true )
        {
            //Stop loading map
            map.close();
            return false;
        }

        //If the number is a valid tile number
        if( ( tileType >= 0 ) && ( tileType < TILE_SPRITES ) )
        {
            tiles[ t ] = new Tile( x, y, tileType );
        }
        //If we don't recognize the tile type
        else
        {
            //Stop loading map
            map.close();
            return false;
        }

        //Move to next tile spot
        x += TILE_WIDTH;

        //If we've gone too far
        if( x >= LEVEL_WIDTH )
        {
            //Move back
            x = 0;

            //Move to the next row
            y += TILE_HEIGHT;
        }
    }

    //Close the file
    map.close();

    //If the map was loaded fine
    return true;
}

bool touches_wall( SDL_Rect box, Tile *tiles[] )
{
    //Go through the tiles
    for( int t = 0; t < TOTAL_TILES; t++ )
    {
        //If the tile is a wall type tile
        if( ( tiles[ t ]->get_type() == TILE_CENTER ) )
        {
            //If the collision box touches the wall tile
            if( check_collision( box, tiles[ t ]->get_box() ) == true )
            {
                return true;
            }
        }
    }

    //If no wall tiles were touched
    return false;
}

Sparkle::Sparkle( int X, int Y )
{
    //Set offsets
    x = X  + ( rand() % 50 );
    y = Y  + ( rand() % 50 );

    //Initialize animation
    frame = rand() % 5;

    //Set type
    switch( rand() % 3 )
    {
        case 0: type = red; break;
        case 1: type = green; break;
        case 2: type = blue; break;
        default:;
    }
}

void Sparkle::show()
{
    //Show image
    apply_surface( x, y, type, screen );

    //Show shimmer
    if( frame % 2 == 0 )
    {
        apply_surface( x, y, shimmer, screen );
    }

    //Animate
    frame++;
}

bool Sparkle::is_dead()
{
    if( frame > 10 )
    {
        return true;
    }

    return false;
}

Tile::Tile( int x, int y, int tileType )
{
    //Get the offsets
    box.x = x;
    box.y = y;

    //Set the collision box
    box.w = TILE_WIDTH;
    box.h = TILE_HEIGHT;

    //Get the tile type
    type = tileType;
}

void Tile::show()
{
    //If the tile is on screen
    if( check_collision( camera, box ) == true )
    {
        //Show the tile
        apply_surface( box.x - camera.x, box.y - camera.y, tileSheet, screen, &clips[ type ] );
    }
}

int Tile::get_type()
{
    return type;
}

SDL_Rect Tile::get_box()
{
    return box;
}

Cat::Cat()
{
    //Initialize the offsets
    box.x = 0;
    box.y = 0;
    box.w = CAT_WIDTH;
    box.h = CAT_HEIGHT;

    //Initialize the velocity
    xVel = 0;
    yVel = 0;

    //Initialize sparkles
    for( int p = 0; p < TOTAL_SPARKLES; p++ )
    {
        sparkles[ p ] = new Sparkle( box.x, box.y );
    }
}

Cat::~Cat()
{
    //Delete sparkles
    for( int p = 0; p < TOTAL_SPARKLES; p++ )
    {
        delete sparkles[ p ];
    }
}

void Cat::handle_input()
{
    if (game_over != true)
    {
        //If a key was pressed
        if( event.type == SDL_KEYDOWN )
        {
            //Adjust the velocity
            switch( event.key.keysym.sym )
            {
                case SDLK_UP: yVel -= CAT_HEIGHT / 5; break;
                case SDLK_DOWN: yVel += CAT_HEIGHT / 5; break;
                case SDLK_LEFT: xVel -= CAT_WIDTH / 5; break;
                case SDLK_RIGHT: xVel += CAT_WIDTH / 5; break;
                default:;
            }
        }
        //If a key was released
        else if( event.type == SDL_KEYUP )
        {
            //Adjust the velocity
            switch( event.key.keysym.sym )
            {
                case SDLK_UP: yVel += CAT_HEIGHT / 5; break;
                case SDLK_DOWN: yVel -= CAT_HEIGHT / 5; break;
                case SDLK_LEFT: xVel += CAT_WIDTH / 5; break;
                case SDLK_RIGHT: xVel -= CAT_WIDTH / 5; break;
                default:;
            }
        }
    }
}

void Cat::move( Tile *tiles[] )
{
    //Move the cat left or right
    box.x += xVel;

    //If the cat went too far to the left or right or touched a wall
    if( ( box.x < 0 ) || ( box.x + CAT_WIDTH > LEVEL_WIDTH ) || touches_wall( box, tiles ) )
    {
        //move back
        box.x -= xVel;
    }

    //Move the cat up or down
    box.y += yVel;

    //If the cat went too far up or down or touched a wall
    if( ( box.y < 0 ) || ( box.y + CAT_HEIGHT > LEVEL_HEIGHT ) || touches_wall( box, tiles ) )
    {
        //move back
        box.y -= yVel;
    }

    if ( box.y < TILE_HEIGHT && box.x > (LEVEL_WIDTH - TILE_WIDTH) )
    {
        // win the game
        game_win = true;
    }

}

void Cat::show_sparkles()
{
    //Go through sparkles
    for( int p = 0; p < TOTAL_SPARKLES; p++ )
    {
        //Delete and replace dead sparkles
        if( sparkles[ p ]->is_dead() == true )
        {
            delete sparkles[ p ];

            sparkles[ p ] = new Sparkle( box.x - camera.x, box.y - camera.y );
        }
    }

    //Show sparkles
    for( int p = 0; p < TOTAL_SPARKLES; p++ )
    {
        sparkles[ p ]->show();
    }
}

void Cat::show()
{
    //If Cat is moving left
    if( xVel < 0 )
    {
        apply_surface( box.x - camera.x, box.y - camera.y, leftCat, screen );
    }
    //If Car is moving right
    else if( xVel > 0 )
    {
        apply_surface( box.x - camera.x, box.y - camera.y, cat, screen );
    }
    //If Cat is moving up
    else if( yVel < 0 )
    {
        apply_surface( box.x - camera.x, box.y - camera.y, upCat, screen );
    }
    //If Car is moving down
    else if( yVel > 0 )
    {
        apply_surface( box.x - camera.x, box.y - camera.y, downCat, screen );
    }
    else // cat is standing still
    {
        apply_surface( box.x - camera.x, box.y - camera.y, cat, screen );
    }


    //Show the sparkles
    show_sparkles();
}

void Cat::set_camera()
{
    //Center the camera over the cat
    camera.x = ( box.x + CAT_WIDTH / 2 ) - SCREEN_WIDTH / 2;
    camera.y = ( box.y + CAT_HEIGHT / 2 ) - SCREEN_HEIGHT / 2;

    //Keep the camera in bounds.
    if( camera.x < 0 )
    {
        camera.x = 0;
    }
    if( camera.y < 0 )
    {
        camera.y = 0;
    }
    if( camera.x > LEVEL_WIDTH - camera.w )
    {
        camera.x = LEVEL_WIDTH - camera.w;
    }
    if( camera.y > LEVEL_HEIGHT - camera.h )
    {
        camera.y = LEVEL_HEIGHT - camera.h;
    }
}

Timer::Timer()
{
    //Initialize the variables
    startTicks = 0;
    pausedTicks = 0;
    paused = false;
    started = false;
}

void Timer::start()
{
    //Start the timer
    started = true;

    //Unpause the timer
    paused = false;

    //Get the current clock time
    startTicks = SDL_GetTicks();
}

void Timer::stop()
{
    //Stop the timer
    started = false;

    //Unpause the timer
    paused = false;
}

void Timer::pause()
{
    //If the timer is running and isn't already paused
    if( ( started == true ) && ( paused == false ) )
    {
        //Pause the timer
        paused = true;

        //Calculate the paused ticks
        pausedTicks = SDL_GetTicks() - startTicks;
    }
}

void Timer::unpause()
{
    //If the timer is paused
    if( paused == true )
    {
        //Unpause the timer
        paused = false;

        //Reset the starting ticks
        startTicks = SDL_GetTicks() - pausedTicks;

        //Reset the paused ticks
        pausedTicks = 0;
    }
}

int Timer::get_ticks()
{
    //If the timer is running
    if( started == true )
    {
        //If the timer is paused
        if( paused == true )
        {
            //Return the number of ticks when the timer was paused
            return pausedTicks;
        }
        else
        {
            //Return the current time minus the start time
            return SDL_GetTicks() - startTicks;
        }
    }

    //If the timer isn't running
    return 0;
}

bool Timer::is_started()
{
    return started;
}

bool Timer::is_paused()
{
    return paused;
}

int main( int argc, char* args[] )
{
    //The cat
    Cat myCat;

    //The tiles that will be used
    Tile *tiles[ TOTAL_TILES ];

    //The frame rate regulator
    Timer fps;

    //The timer starting time
    Uint32 start = 0;

    bool running = true;

    //Initialize
    if( init() == false )
    {
        return 1;
    }

    //Load the files
    if( load_files() == false )
    {
        return 1;
    }

    //Clip the tile sheet
    clip_tiles();

    //Set the tiles
    if( set_tiles( tiles ) == false )
    {
        return 1;
    }

    //Start the timer @ 22 seconds
    start = 25000;

    //While the user hasn't quit
    while( quit == false )
    {
        //Start the frame timer
        fps.start();

        //While there's events to handle
        while( SDL_PollEvent( &event ) )
        {
            //Handle events for the cat
            myCat.handle_input();

            //If the user has Xed out the window
            if( event.type == SDL_QUIT )
            {
                //Quit the program
                quit = true;
            }
        }

        //Move the cat
        myCat.move( tiles );

        //Set the camera
        myCat.set_camera();

        //Show the tiles
        for( int t = 0; t < TOTAL_TILES; t++ )
        {
            tiles[ t ]->show();
        }

        //Show the cat on the screen
        myCat.show();

        //If the timer is running
        if( running == true )
        {
            //If there is no music playing
            if( Mix_PlayingMusic() == 0 )
            {
                //Play the music
                if( Mix_PlayMusic( musicIngame, 0 ) == -1 )
                {
                    return 1;
                }
            }

            int currentTime = start - SDL_GetTicks();

            //The timer's time as a string
            std::stringstream time;

            //Convert the timer's time to a string
            time << "Timer: " << currentTime;

            // end game after time limit reached
            if ( currentTime <= 0 )
            {
                //Stop the music
                Mix_HaltMusic();

                game_over = true;
                running = false;


            }
            if( game_win == true )
            {
                Mix_HaltMusic();
            }

            //Render the time surface
            seconds = TTF_RenderText_Solid( font, time.str().c_str(), textColor );

            //Apply the time surface
            apply_surface( ( SCREEN_WIDTH - seconds->w ) / 2, seconds->h, seconds, screen );

            //Free the time surface
            SDL_FreeSurface( seconds );
        }

        if( game_over == true )
        {
            //Generate the message surface
            gameOver = TTF_RenderText_Solid( fontGA, "GAME OVER", textColor );

            //Apply the message
            apply_surface( ( SCREEN_WIDTH - gameOver->w ) / 2, 200, gameOver, screen );

            //If there is no music playing
            if( Mix_PlayingMusic() == 0 )
            {
                Mix_PlayMusic( musicDeath, 0 );
            }

            // stop cat's movement
            myCat.xVel = 0;
            myCat.yVel = 0;

        }

        if( game_win == true )
        {
            // stop timer
            running = false;

            //Generate the message surface
            gameOver = TTF_RenderText_Solid( fontGA, "YOU WIN !!", textColor );

            //Apply the message
            apply_surface( ( SCREEN_WIDTH - gameOver->w ) / 2, 200, gameOver, screen );

            //If there is no music playing
            if( Mix_PlayingMusic() == 0 )
            {
                //Play the music
                 Mix_PlayMusic( music, -1 );

            }

        }


        //Update the screen
        if( SDL_Flip( screen ) == -1 )
        {
            return 1;
        }

        //Cap the frame rate
        if( fps.get_ticks() < 1000 / FRAMES_PER_SECOND )
        {
            SDL_Delay( ( 1000 / FRAMES_PER_SECOND ) - fps.get_ticks() );
        }
    }

    //Clean up
    clean_up( tiles );

    return 0;
}
