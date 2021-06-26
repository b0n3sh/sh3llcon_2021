#!venv/bin/python3

import numpy, cv2, imutils, easyocr
from matplotlib import pyplot

img = 'main.jpg'    # Path de la imagen que vamos a procesar.

def show_image(img):            # Función que nos muestra la imagen en una ventana nueva,
    cv2.imshow('title', img)   # para cerrar la ventana, simplemente presionamos cualquier tecla.
    cv2.waitKey(0)

def find_rectangle(contours):
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            return approx, approx 

img = cv2.imread(img) # Cargamos la imagen en la variable como un objeto cv2.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Pasamos a blanco y negro la imagen.
show_image(gray)
bfilter = cv2.bilateralFilter(gray, 100, 20, 20) # Reducimos el ruido de la imagen.
show_image(bfilter)
edged = cv2.Canny(bfilter, 30, 200) # Con este algoritmo, buscamos las esquinas de la imagen.
show_image(edged)
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Agrupamos los puntos que forman el contorno de forma jerárquica.
contours = imutils.grab_contours(keypoints) # Los metemos en la variable, bien formateado, gracias a imutils.
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] # Los ordenamos de mayor a menor, cogiendo solo un slice de los 10 primeros. 

location, approx = find_rectangle(contours)

mask = numpy.zeros(gray.shape, numpy.uint8)
new_image = cv2.drawContours(mask, [location], 0,255, -1) # Creamos un rectángulo blanco en el area donde presuponemos que está la matrícula.
new_image = cv2.bitwise_and(img, img, mask=mask) # Con un AND, hacemos un MERGE de la imagen, dibujando solo el rectángulo de la matrícula.
show_image(new_image)

(x,y) = numpy.where(mask==255)          # Buscamos la delimitación de dónde se encuentra la matrícula y recortamos la imagen
(x1, y1) = (numpy.min(x), numpy.min(y))      
(x2, y2) = (numpy.max(x), numpy.max(y)) 
cropped_image = gray[x1:x2+1, y1:y2+1] 

reader = easyocr.Reader(['en'])         # Lectura OCR
result = reader.readtext(cropped_image)
text = result[0][-2]
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3) # Añadimos un overlay sobre la matrícula con el string y lo resaltamos en verde.

show_image(res)
print(text)
