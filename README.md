# Challenge Data Engineer LATAM

Crear funciones para distintas situaciones, optimizadas para el uso de memoria o el tiempo de ejecucion segun corresponda.

## Índice

1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Resultados de Rendimiento](#resultados-de-rendimiento)
6. [Discusión](#discusión)

## Descripción

Este repositorio cuenta con una notebook **soluciones.ipynb** donde tenemos un pequeño EDA del file .json en este caso el nombre es **tweets.json**. Ademas, contiene todas las funciones requeridas para las 3 preguntas con su output y una pequeña descripcion del objetivo y caracteristicas principales.
Por ultimo, esta el archivo **soluciones.py** que te va a permitir ejecutar estas funciones y evaluarlas.

## Requisitos

- python 3.8
- emoji
- pandas
- memory-profiler
- ujson
- ipykernel

## Instalación

```bash
git clone https://github.com/gonbat/latam_dataeng
cd latam_dataeng
pip install -r requirements.txt
```
## Uso

Para ejecutar las funciones hay que ejecutar el file **soluciones.py**  pasandole el nombre de la funcion q1_time por ejemplo. Esto va a devolver el tiempo que tarda en ejecutarse esta funcion:

```bash
python soluciones.py q1_time
```
Para obtener mas informacion sobre el contenido del file podes ejecutar en la terminal:

```bash
python soluciones.py --h
```
Esto te va a retornar lo siguiente:

```bash
usage: soluciones.py [-h] [--file_path FILE_PATH] {q1_memory,q1_time,q2_memory,q2_time,q3_memory,q3_time}

Funciones optimizadas para memoria o tiempo de ejecucion; Challenge Data Engineer

positional arguments:
  {q1_memory,q1_time,q2_memory,q2_time,q3_memory,q3_time}
                        Selecciona la función a ejecutar

optional arguments:
  -h, --help            show this help message and exit
  --file_path FILE_PATH
                        Valor por defecto para file_path es: tweets.json
```

Si queres modificar las funciones podes hacerlo desde **soluciones.ipynb**, donde vas a encontrar las funciones ordenadas por orden, una descripcion y el output de las mismas; luego podes copiar y pegar el nuevo codigo en **soluciones.py** y realizar la prueba que consideres. 

## Resultados de Rendimiento

Para medir el rendimiento de las funciones en memoria use 'memory-profiler' y para el rendimiento de tiempo utilice 'cProfile' y 'pstats'.

 - q1_time

```bash
Total execution time in seconds: 9.25
```
- q1_memory

```bash
Memory usage in MB (in chunks of  1 seconds): [51.34765625, 51.34765625, 51.72265625, 51.84765625, 51.84765625, 51.84765625, 52.34765625, 52.34765625, 52.47265625, 52.47265625, 52.47265625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625, 52.59765625]
Maximum memory usage in MB: 52.59765625
```

- q2_time

```bash
Total execution time in seconds: 10.74
```
- q2_memory

```bash
Memory usage in MB (in chunks of  1 seconds): [51.22265625, 51.22265625, 51.72265625, 51.72265625, 51.72265625, 51.72265625]
Maximum memory usage in MB: 51.72265625
```

- q3_time

```bash
Total execution time in seconds: 23.43
```

- q3_memory

```bash
Memory usage in MB (in chunks of  1 seconds): [51.2265625, 51.2265625, 52.4765625, 53.3515625, 53.95703125]
Maximum memory usage in MB: 53.95703125
```

## Discusión

Se implemento todas las funciones usando Python puro, que funciono muy bien para estas funciones pero si hubiera que escalarlo se podria pensar en otras alternativas; listo algunas:

1. Paralelización y Distribución:
  - Dask: Es ideal para paralelizacion en una sola maquina o en un cluster.
  - Pyspark: Mas adecuado para clusteres mas grandes, y tien un ecosistema muy amplio.

2. Librerias especializadas:
  - Pyarrow: Permite un rápido procesamiento del archivo JSON, sino que también es muy útil para trabajar con datos en formatos como Parquet, lo cual es muy eficiente en términos de almacenamiento y velocidad de consulta.

3. Servicios en la nube:

  - Google Cloud Functions + Google Cloud Storage:  Si ya estas usando GCP o necesitas una solución que se pueda escalar automáticamente sin necesidad de gestionar servidores.