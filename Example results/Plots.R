library(ggplot2)
library(tidyr)

data <- read.csv("./datos.csv")
data$Hora <- str_extract(data$fecha_hora, "(?<= ).+")
#data$fecha_hora <- hms(data$fecha_hora)
data$Hora <- as.POSIXct(data$Hora, format="%H:%M:%S")


ggplot(data) + geom_line(aes(x = Hora, y =  trafico)) + 
  geom_vline(xintercept = as.POSIXct("15:08:00", format="%H:%M:%S"), col = "red") +
  ylab("Tráfico (nº tweets)") + theme_light()
ggplot(data) + geom_line(aes(x = Hora, y =  polaridad)) + 
  geom_vline(xintercept = as.POSIXct("15:08:00", format="%H:%M:%S"), col = "red") +
  ylab("Polaridad") + theme_light()
ggplot(data) + geom_line(aes(x = Hora, y =  subjetividad)) + 
  geom_vline(xintercept = as.POSIXct("15:08:00", format="%H:%M:%S"), col = "red") +
  ylab("Subjetividad") + theme_light()
