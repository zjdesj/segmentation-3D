library(readxl)
library(ggplot2)
library(patchwork)

setwd("/Users/wyw/Documents/Chaper2/github-code/segmentation-3D/data-result")

data <- read_excel('results-campaigns.xlsx')
data$date <- factor(data$date, labels = c('afternoon on 8 Jan.', 'morning on 9 Jan.', 'night on 31 Dec.', 'afternoon on 9 Jan.'))
data$height <- factor(data$height, levels=c('8', '10', '15', '30', '50', 'n8','n10', 'n15')
                      , labels = c('8m', '10m', '15m', '30m', '50m', '8m at night', '10m at night', '15m at night'))
data$height
data$points = data$points / 1000000
data$points
head(data, n=5)

camaign_size = ggplot(data, aes(x = duration, y = points, group=height)) + 
  geom_line(aes(col = height)) +
  geom_point(aes(col = height)) +
  theme_minimal() +
  theme(legend.position = c(0.1, 0.8) ) +
  labs(x = "Duration of acqusition in campaign (unit: sencond)", 
       y = "Point cloud size (unit: million)",
       col = "Height Category"
  ) 

camaign_size



campaign_time = ggplot(data, aes(x = time, y = `standing cattle`, group = date, color = date)) +
  geom_line(aes(linetype = "Standing cattle")) +
  geom_point() +
  geom_line(aes(y = `avaliable cattle`, linetype = "Seleted standing cattle")) +
  geom_point(aes(y = `avaliable cattle`)) + 
  scale_color_manual(values = c("blue", "red", "green", "purple"), guide = guide_legend(title = "Time slots")) +
  scale_linetype_manual(values = c( "dashed", "solid")) +
  theme_minimal() +
  theme(legend.position = c(0.91, 0.75) ) +
  labs(x = "Time of implementing campaign", y = "Cattle size") +
  guides(linetype = guide_legend(title = "Cattle size"))

campaign_time



ggplot(data, aes(x = time, y = `max-illumiantion`, group = date, color = date)) +
  geom_line(aes(linetype = "maximum light strength")) +
  #geom_point() +
  geom_line(aes(y = `min-illumiantion`, linetype = "minimum light strength")) +
  #geom_point(aes(y = `min-illumiantion`)) + 
  scale_color_manual(values = c("blue", "red", "green", "purple"), guide = guide_legend(title = "Time slots")) +
  scale_linetype_manual(values = c("solid", "dashed")) +
  theme_minimal() +
  theme(legend.position = c(0.91, 0.75) ) +
  labs(x = "Enviroment of implementing campaign", y = "Light strength (x1000 lux)") +
  guides(linetype = guide_legend(title = "Cattle size"))

  
