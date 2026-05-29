# Renombrador de facturas PDF

Aplicaciones de escritorio en Tkinter para renombrar facturas PDF tipo A y tipo B.

Cada script lee la primera pagina del PDF, busca el patron de factura `XXXX-XXXXXXXX` y renombra el archivo con el formato correspondiente.

## Scripts

- `renombrar_A.py`: facturas tipo A
- `renombrar_B.py`: facturas tipo B

## Generar ejecutables

En una computadora con Python:

```bat
compilar_exe.bat
```

Los ejecutables se generan en `dist_final/`.

