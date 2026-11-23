#include <genesis.h>
#include "graphics.h"

// Jorge Truck Driver: versao grafica pixel art para Mega Drive.
// Arte original 4 bits por pixel, 16 cores, tela 320 x 224.
// Graficos gerados por tools/generate_art.py durante a compilacao.

#define LANES 3
#define OBJECTS 6
#define PLAYER_X 5
#define SPAWN_X 38

typedef struct {
    s16 x;
    u8 lane;
    u8 kind;   // 0 = caixa, 1 = rocha, 2 = cone
    u8 active;
} TruckObject;

static TruckObject objects[OBJECTS];
static const u16 laneY[LANES] = {13,18,23};
static u16 seed = 0x2A37;
static u16 lastButtons = 0;
static s16 score = 0;
static u16 lives = 5;
static u8 lane = 1;
static u8 speed = 2;
static u8 gameState = 0;   // 0 menu, 1 jogando, 2 pausa, 3 game over
static u16 moveTicks=0, spawnTicks=0;

static u16 randomNumber(void)
{
    seed = (u16) (seed * 109u + 1021u);
    return seed;
}

// So escreve tiles em BG_A, preservando todo o fundo em BG_B.
static void drawSprite(const u16 *map, u16 w, u16 h, u16 x, u16 y)
{
    u16 tx,ty;
    for (ty=0; ty<h; ty++)
        for (tx=0; tx<w; tx++)
            if (x+tx<40 && y+ty<28)
                VDP_setTileMapXY(BG_A, TILE_ATTR_FULL(PAL1, TRUE, FALSE, FALSE,
                    TILE_USER_INDEX+map[ty*w+tx]), x+tx,y+ty);
}

static void drawWorld(void)
{
    u16 x,y;
    char hud[40];
    // O fundo se desenha uma so vez: leve para o hardware 16 bits.
    VDP_setScreenWidth320();
    VDP_clearPlane(BG_A, TRUE);
    VDP_clearPlane(BG_B, TRUE);
    PAL_setPalette(PAL1, gfxPalette, DMA);
    VDP_loadTileData(gfxTiles,TILE_USER_INDEX,GFX_TILE_COUNT,DMA);

    for (y=0;y<28;y++)
        for (x=0;x<40;x++)
            VDP_setTileMapXY(BG_B,TILE_ATTR_FULL(PAL1,FALSE,FALSE,FALSE,
                TILE_USER_INDEX+gfxBgMap[y*40+x]),x,y);
    VDP_setTextPlane(BG_A);
    VDP_setTextPalette(PAL0);
    VDP_drawText("JORGE TRUCK DRIVER  -  16 BIT",2,1);
    VDP_drawText("RIO DE JANEIRO",2,3);
    sprintf(hud,"CAIXAS +1    PERDIDAS -3");
    VDP_drawText(hud,2,7);
}

static void resetGame(void)
{
    u16 i;
    gameState=1;
    lives=5; score=0;lane=1;speed=2;moveTicks=0;spawnTicks=0;
    seed+=31;
    for(i=0;i<OBJECTS;i++) objects[i].active=0;
}

static void spawnObject(void)
{
    u16 i;
    for(i=0;i<OBJECTS;i++)
        if(!objects[i].active)
        {
            objects[i].active=1;
            objects[i].x=SPAWN_X;
            objects[i].lane=(u8)(randomNumber()%LANES);
            objects[i].kind=(u8)((randomNumber()%4)==0 ? (1+(randomNumber()&1)) : 0);
            break;
        }
}

static void advanceObjects(void)
{
    u16 i;
    for (i=0;i<OBJECTS;i++)
    {
        TruckObject *o=&objects[i];
        if (!o->active) continue;
        o->x--;
        if(o->lane==lane && o->x>=PLAYER_X && o->x<=PLAYER_X+6)
        {
            if(o->kind==0) score++;
            else if (lives>0) lives--;
            o->active=0;
        }
        else if(o->x<1)
        {
            if(o->kind==0)
            {
                score-=3;
                if(score<0)score=0;
            }
            o->active=0;
        }
    }
    if(lives==0)gameState=3;
}

static void render(void)
{
    u16 i;
    char hud[40];

    // Remove os sprites antigos, mas mantem o cenario em BG_B.
    VDP_clearTileMapRect(BG_A,0,12,40,16);
    for(i=0;i<OBJECTS;i++)
    {
        TruckObject *o=&objects[i];
        if(o->active && o->x < 39 && o->x>=0)
            drawSprite(o->kind==0?gfxCrate:(o->kind==1?gfxRock:gfxCone),
                       2,2,(u16)o->x,laneY[o->lane]+1);
    }

    drawSprite(gfxTruck,6,3,PLAYER_X,laneY[lane]);

    VDP_drawText("                                     ",1,5);
    sprintf(hud,"PONTOS:%5d  VIDAS:%u  VEL:%u",score,lives,speed);
    VDP_drawText(hud,1,5);

    if(gameState==0) VDP_drawText("START OU A PARA JOGAR",7,26);
    else if(gameState==2) VDP_drawText("PAUSADO  -  START RETOMA",6,26);
    else if(gameState==3) VDP_drawText("FIM!  START REINICIA",8,26);
    else VDP_drawText("A/C GAS  B FREIO  CIMA/BAIXO",3,26);
}

int main(bool hard)
{
    u16 keys,pressed;
    bool redraw=TRUE;
    (void)hard;

    JOY_init();
    drawWorld();
    render();

    while(1)
    {
        keys=JOY_readJoypad(JOY_1);
        pressed=keys&(u16)~lastButtons;
        lastButtons=keys;

        if(gameState==0 || gameState==3)
        {
            if(pressed&(BUTTON_START|BUTTON_A)) {resetGame();redraw=TRUE;}
        }
        else if(gameState==2)
        {
            if(pressed&BUTTON_START){gameState=1;redraw=TRUE;}
        }
        else
        {
            if(pressed&BUTTON_START) {gameState=2;redraw=TRUE;}
            else
            {
                if((pressed&BUTTON_UP)&&lane>0){lane--;redraw=TRUE;}
                if((pressed&BUTTON_DOWN)&&lane<2){lane++;redraw=TRUE;}
                if((keys&(BUTTON_A|BUTTON_C))&&speed<4) speed++;
                if((keys&BUTTON_B)&&speed>1) speed--;
                if((keys&(BUTTON_A|BUTTON_B|BUTTON_C))==0) speed=2;

                moveTicks++;
                if(moveTicks>=(u16)(13-speed*2))
                {
                    moveTicks=0;
                    spawnTicks++;
                    advanceObjects();
                    if(gameState==1 && spawnTicks>=8)
                    {
                        spawnTicks=0;
                        spawnObject();
                    }
                    redraw=TRUE;
                }
            }
        }

        if(redraw)
        {
            render();
            redraw=FALSE;
        }
        SYS_doVBlankProcess();
    }
    return 0;
}
