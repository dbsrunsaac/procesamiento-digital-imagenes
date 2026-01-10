# --------------------------------------------
# Autor: Ruben Dario Florez Zela
# Fecha: 01 de febrero de 2025
# Descripción: Codigo para realizar concatenacion
#              de imagenes y videos en un panlel
#              didactico e interactivo.
# Contacto: ruben.florez@unsaac.edu.pe
#
# Licencia: MIT
#
# Copyright (c) 2025 Ruben Dario Florez Zela
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------

import cv2
import numpy as np

def crear_panel(imagenes, etiquetas, filas, columnas, tamaño_base=200, escala_panel=100):
    ancho_panel = columnas * tamaño_base
    alto_panel = filas * tamaño_base
    
    total_celdas = filas * columnas
    while len(imagenes) < total_celdas:
        imagenes.append(np.zeros((tamaño_base, tamaño_base, 3), dtype=np.uint8))
        etiquetas.append("no image")
    
    celdas = []
    for img, etiqueta in zip(imagenes, etiquetas):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
        h, w = img.shape[:2]
        escala = min(1.0, tamaño_base/w, tamaño_base/h)
        img_resized = cv2.resize(img, (0,0), fx=escala, fy=escala)
        
        canvas = np.zeros((tamaño_base, tamaño_base, 3), dtype=np.uint8)
        
        y_offset = (tamaño_base - img_resized.shape[0]) // 2
        x_offset = (tamaño_base - img_resized.shape[1]) // 2
        canvas[y_offset:y_offset+img_resized.shape[0], 
               x_offset:x_offset+img_resized.shape[1]] = img_resized
        
        cv2.putText(canvas, etiqueta, (10, 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        
        celdas.append(canvas)
    
    panel_filas = []
    for i in range(0, len(celdas), columnas):
        fila = np.hstack(celdas[i:i+columnas])
        panel_filas.append(fila)
    
    panel = np.vstack(panel_filas[:filas])
    
    if escala_panel != 100:
        panel = cv2.resize(panel, (0,0), 
                          fx=escala_panel/100, 
                          fy=escala_panel/100)
    
    return panel