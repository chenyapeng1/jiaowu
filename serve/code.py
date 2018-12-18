from PIL import Image,ImageDraw,ImageFont
import random
import io

class code:
    def __init__(self):
        self.width=120
        self.height=40
        self.im=None
        self.lineNum=None
        self.pointNum=None
        self.codecon="QWERTYUPASDFGHJKZXCVBNMqwertyupadfhkzxcvbnm0123456789"
        self.codelen=4
        self.str=""
    def randBgColor(self):
        return (random.randint(0,120),random.randint(0,120),random.randint(0,120))
    def randFgColor(self):
        return (random.randint(120, 255), random.randint(120, 255), random.randint(120, 255))
    def create(self):
        self.im = Image.new('RGB', size=(self.width, self.height), color=self.randBgColor())
    def lines(self):
        lineNum=self.lineNum or random.randint(3,6)
        draw = ImageDraw.Draw(self.im)
        for item in range(lineNum):
            place=(random.randint(0,self.width),random.randint(0,self.height),random.randint(0,self.height),random.randint(0,self.height))
            draw.line(place,fill=self.randFgColor(),width=random.randint(1,3))
    def point(self):
        pointNum = self.pointNum or random.randint(30, 60)
        draw = ImageDraw.Draw(self.im)
        for item in range(pointNum):
            place=(random.randint(0,self.width),random.randint(0,self.height))
            draw.point(place,fill=self.randFgColor())
    def texts(self):
        draw = ImageDraw.Draw(self.im)
        for item in range(self.codelen):
            x=item*self.width/self.codelen+random.randint(-self.width/15,self.width/15)
            y=random.randint(-self.height/10,self.height/10)
            text=self.codecon[random.randint(0,len(self.codecon)-1)]
            self.str+=text
            fnt = ImageFont.truetype('C:\WINDOWS\Fonts\ARVO-REGULAR.TTF', random.randint(30,38))
            draw.text((x,y),text,fill=self.randFgColor(),font=fnt,rotate="180")
    def output(self):
        self.create()
        self.texts()
        self.lines()
        self.point()
        bt=io.BytesIO()
        self.im.save(bt,"png")
        return bt.getvalue()

