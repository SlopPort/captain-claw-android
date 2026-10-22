"""Generate original credit cards using only Python's standard library.

Text, layout and the small uppercase bitmap alphabet were written by OpenAI
Codex. No game artwork, screenshots or third-party font files are copied.
This source follows the adaptation's GPL-3.0 license.
"""
import struct
import zlib

# Five-bit rows, seven rows per glyph. Keeping this small alphabet in source
# makes packaging independent of installed system fonts and image libraries.
FONT={
 'A':[14,17,17,31,17,17,17], 'B':[30,17,17,30,17,17,30],
 'C':[14,17,16,16,16,17,14], 'D':[30,17,17,17,17,17,30],
 'E':[31,16,16,30,16,16,31], 'F':[31,16,16,30,16,16,16],
 'G':[14,17,16,23,17,17,15], 'H':[17,17,17,31,17,17,17],
 'I':[14,4,4,4,4,4,14], 'J':[7,2,2,2,18,18,12],
 'K':[17,18,20,24,20,18,17], 'L':[16,16,16,16,16,16,31],
 'M':[17,27,21,21,17,17,17], 'N':[17,25,21,19,17,17,17],
 'O':[14,17,17,17,17,17,14], 'P':[30,17,17,30,16,16,16],
 'Q':[14,17,17,17,21,18,13], 'R':[30,17,17,30,20,18,17],
 'S':[15,16,16,14,1,1,30], 'T':[31,4,4,4,4,4,4],
 'U':[17,17,17,17,17,17,14], 'V':[17,17,17,17,17,10,4],
 'W':[17,17,17,21,21,21,10], 'X':[17,17,10,4,10,17,17],
 'Y':[17,17,10,4,4,4,4], 'Z':[31,1,2,4,8,16,31],
 '2':[14,17,1,2,4,8,31], '3':[30,1,1,14,1,1,30],
 ' ': [0]*7, '/':[1,2,2,4,8,8,16], '-':[0,0,0,31,0,0,0],
 '.':[0,0,0,0,0,12,12], ':':[0,12,12,0,12,12,0],
}


def card(title,lines):
    width,height=256,240
    pixels=bytearray(bytes((20,28,40,255))*width*height)
    def text(value,x,y,scale=1,color=(225,231,240,255)):
        assert x+len(value)*6*scale<=width-8,value
        for char in value:
            for row,bits in enumerate(FONT[char]):
                for col in range(5):
                    if bits & (1<<(4-col)):
                        for dy in range(scale):
                            for dx in range(scale):
                                offset=((y+row*scale+dy)*width+x+col*scale+dx)*4
                                pixels[offset:offset+4]=bytes(color)
            x+=6*scale
    text(title,12,14,2,(245,200,100,255))
    for index,line in enumerate(lines):text(line,12,48+index*14)
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    raw=b''.join(b'\0'+pixels[y*width*4:(y+1)*width*4] for y in range(height))
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))
            +chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))


def credit_cards():
    return card('OPEN SOURCE',[
        'OPENCLAW: PJASICEK AND CONTRIBUTORS',
        'CLAW WEB: ARTHUR BOSS AND CONTRIBUTORS',
        '', 'SDL / SDL IMAGE / SDL MIXER',
        'SDL TTF / SDL GFX', 'BOX2D / LIBWAP / TINYXML',
        'FREETYPE / FREEPATS / TIMIDITY', 'SDL GAMECONTROLLERDB',
        '', 'FULL ATTRIBUTION AND LICENSES:', 'NOTICE.MD / LICENSES IN APK',
    ]),card('ANDROID PORT',[
        'CODE AND TESTS: OPENAI CODEX',
        'LLM WORK WITH HUMAN FEEDBACK',
        '', 'ENGINE AND PORT: GPL 3',
        'DEPENDENCIES KEEP THEIR LICENSES',
        '', 'CLAW: MONOLITH PRODUCTIONS',
        'GAME DATA REMAINS COPYRIGHTED',
        'USER SUPPLIES OWN GAME DATA',
        '', 'ORIGINAL CREDIT CARDS BY CODEX',
    ])
