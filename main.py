import cv2,sys,time

def GetFrames(file,every_nth_frame): #extracts frames from the hockey video
  capture = cv2.VideoCapture(file)
  frameNr = 0
  frames = []
  while True:
    success, frame = capture.read()
    if success:
      if frameNr%every_nth_frame == 0:
        frames.append(frame)
    else:
      break
    frameNr = frameNr+1
  capture.release()
  return frames

def ColorPixel(r,g,b): #assigns an ansi code to each colour
  return f"\033[48;2;{r};{g};{b}m "

def Convert(img, x_res, y_res): #converts images to rgb values
  rows,cols,_ = img.shape
  wholeframe = []
  line = []
  for i in range(rows):
    if i%x_res==0:
      for j in range(cols):
        if j%y_res==0:
          b = img.item(i,j,0)
          g = img.item(i,j,1)
          r = img.item(i,j,2)
          line.append([r, g, b])
      wholeframe.append(line)
      line = []
  return wholeframe

#img = cv2.imread('output/60.jpg',1)
converted_Frames = []
for frame in GetFrames("hockey.mp4",1):
  pixels = Convert(frame, 8, 4) # x_res should be twice the y_res for most terminals
  converted_Frames.append(pixels)


def main():
  for frame in converted_Frames:
    sys.stdout.write("\u001b[2000D\u001b[2000A")
    framestr = ""
    for line in range(len(frame)):
      linestr = ""
      for pixel in range(len(frame[0])):
        colors = frame[line][pixel]
        linestr += ColorPixel(colors[0], colors[1], colors[2])
        #stdscr.addstr(0,0, str(colors))
      framestr += linestr + "\n"

    sys.stdout.write(framestr)
    sys.stdout.flush()
    time.sleep(0.03)

main()
print("\033c", end="")