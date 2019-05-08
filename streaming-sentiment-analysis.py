# Inportamos las librerias necesarias 
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from textblob import TextBlob
from pyspark.sql.functions import *
import re

# Establecemos la ventana de recogida de datos en streaming en segundos
freq = 60

def quiet_logs( sc ):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
  logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

# Cremos el contexto de Spark en local utilizando 4 núcleos 
sc = SparkContext("local[4]", "NetworkWordCount")
quiet_logs(sc)

# Creamos el StreamingContext en local con el intervalo establecido anteriormente
ssc = StreamingContext(sc, freq)

# Create DStream that will connect to the stream of input lines from connection to localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
n_lines = lines.count()

# Quitamos de las palabras todos los símbolos que no pertenezcan al alfabeto
# Pasamos todas las letras a letra minúscula
regex = re.compile('[^a-zA-Z ]')

lines = lines.map(lambda line: regex.sub('', line.lower()))

# Sentiment analysis
sent = lines.map(lambda x: (TextBlob(x).sentiment.polarity, TextBlob(x).sentiment.subjectivity, 1))
p = lines.map(lambda x: TextBlob(x).sentiment.polarity)
s = lines.map(lambda x: TextBlob(x).sentiment.subjectivity)

p = p.reduce(lambda x, y: x + y)
s = s.reduce(lambda x, y: x + y)

res = n_lines.union(s)
res = res.union(p)

# Print and save results
name = "datos.csv"
with open(name, "a") as myfile:
    myfile.write("trafico,subjetividad,polaridad,fecha_hora\n")
def tpprint(val, num=3):
    """
    Print the first num elements of each RDD generated in this DStream.
    @param num: the number of elements from the first will be printed.
    """
    def takeAndPrint(time, rdd):
        taken = rdd.take(num + 1)

        print("------------------------------")
        print("Time: %s" % time)
        print("------------------------------")

        idx = 0
        title = ("Tráfico: %s tweets", "Subjetividad: %s", "Polaridad: %s")

        for record in taken[:num]:
            idx = idx + 1
            if idx == 1:
                n = record
                print(title[idx-1] % record)
                with open(name, "a") as myfile:
                     myfile.write(str(record) + ",")
            else:
                print(title[idx-1] % (record/n))
                with open(name, "a") as myfile:
                    myfile.write(str(record/n) + ",")

        if len(taken) > num:
            print("...")
        with open(name, "a") as myfile:
            myfile.write(str(time) + "\n")
        print("")

    val.foreachRDD(takeAndPrint)

tpprint(res)

# Start computation
ssc.start()
ssc.awaitTermination()
