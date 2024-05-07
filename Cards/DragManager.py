class DragManager():

    def __init__(self, canvas, canvasObject, XVar, YVar):
        self.canvas = canvas
        self.canvasObject = canvasObject
        self.cursorX = 0
        self.cursorY = 0
        self.XVar = XVar
        self.YVar = YVar

        self.canvas.tag_bind(self.canvasObject, "<Button-1>", self.on_start)
        self.canvas.tag_bind(self.canvasObject, "<B1-Motion>", self.on_drag)

    def on_start(self, event):
        self.cursorX = event.x - int(self.XVar.get())
        self.cursorY = event.y - int(self.YVar.get())

    def on_drag(self, event):
        self.XVar.set(f'{event.x - self.cursorX}')
        self.YVar.set(f'{event.y - self.cursorY}')
