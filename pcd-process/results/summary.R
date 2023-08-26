library(readxl)
library(dplyr)
library(ggplot2)
library(patchwork)

#path = '/Users/wyw/Documents/Chaper2/github-code/segmentation-3D/data-result/results-height&width.xlsx'
setwd("/Users/wyw/Documents/Chaper2/github-code/segmentation-3D/data-result")

data <- read_excel('results-height&width.xlsx')
data$height = factor(data$height, levels=c('8', '10', '15', '30', '50', 'n8', 'n10', 'n15'))
data$speed = factor(data$speed, levels = c('1', '2', '3', '5', '7', '9'), 
                    labels = c('1 m/s', '2 m/s', '3 m/s', '5 m/s', '7 m/s', '9 m/s'))
#summary(data)

for (bm in c('AW', 'HH', 'WH', 'WiH', 'BH')) {
  p1 = ggplot(data, aes_string(x="height",y=bm,fill="height")) +
    geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
    facet_wrap(~speed)+ 
    theme(axis.text.x = element_text(angle = 45,hjust = 1)) +
    labs(y='') 
  
  p2 = ggplot(data, aes_string(x="height",y=bm,fill="height")) +
    geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
    labs(y='')
  
  p3 = ggplot(data, aes_string(x="speed",y=bm,fill="speed")) +
    geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
    labs(y='')
  
  (p2 / p3 | p1) + plot_layout(widths = c(2, 3), heights = c(1))
  
  ggsave(paste('/Users/wyw/Downloads/chapter2-figures/results/data-summary-3in1-', bm, '.png', sep = ''))
}



for (bm in c('AW', 'HH', 'WH', 'WiH', 'BH')) {
  p1 = data %>% 
    ggplot(aes_string(x="height",y=bm,fill="height")) +
    geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
    facet_wrap(~speed) +
    theme(axis.text.x = element_text(angle = 45,hjust = 1))
  ggsave(paste('/Users/wyw/Downloads/chapter2-figures/results/data-summary-', bm, '.png', sep = ''))
  
  p2 = data %>% ggplot(aes_string(x="height",y=bm,fill="height")) +
    geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2)
  ggsave(paste('/Users/wyw/Downloads/chapter2-figures/results/data-summary-height-', bm, '.png', sep = ''))
  
  p3 = data %>% ggplot(aes_string(x="speed",y=bm,fill="speed")) +
    geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2)
  ggsave(paste('/Users/wyw/Downloads/chapter2-figures/results/data-summary-speed-', bm, '.png', sep = ''))
}


data_day = data[1:235,2:ncol(data)]
data_day$height = factor(data_day$height, levels=c('8', '10', '15', '30', '50'))
data_day$speed = factor(data_day$speed, levels = c('1', '2', '3', '5', '7', '9'))
summary(data_day)

data_night = data[236:275,2:ncol(data)]
data_night$height = factor(data_night$height, levels = c('n8', 'n10', 'n15'))
data_night$speed = factor(data_night$speed, levels = c('3', '5'))
summary(data_night)

campaign = group_by(data_day, height, speed)
summarise(campaign, 
    width_mean = mean(width),
    width_sd = sd(width)      
)


# Create a grouped boxplot with facets for each response
#ggplot(data, aes(x = $, y = Response1, fill = Factor2)) +
#  geom_boxplot() +
#  facet_grid(. ~ Response2) +
#  labs(title = "Grouped Boxplot by Two Factors and Responses",
#       x = "Factor 1", y = "Response 1") +
#  theme_minimal()


#data_day %>%
#  ggplot(aes(x=height,y=width,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
#data_night %>%
#  ggplot(aes(x=height,y=width,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
#data %>%
#  ggplot(aes(x=height,y=width,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
##belly width (no correction)
#data %>%
#  ggplot(aes(x=height,y=width,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
##belly width(correction)
#data %>%
#  ggplot(aes(x=height,y=Rwidth,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
##belly width(no filter)
#data %>%
#  ggplot(aes(x=height,y=widthNopure,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
##hip height(bounding box)
#data %>%
#  ggplot(aes(x=height,y=HH1,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
##hip height(spine)
#data %>%
#  ggplot(aes(x=height,y=HH2,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
##waist height
#data %>%
#  ggplot(aes(x=height,y=WH,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
## wither height (60)
#data %>%
#  ggplot(aes(x=height,y=WiH1,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
## wither height (55)
#data %>%
#  ggplot(aes_string(x="height",y="WiH2",fill="height")) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
## back height
#data %>%
#  ggplot(aes(x=height,y=BH,fill=height)) +
#  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
#  facet_wrap(~speed) +
#  theme(axis.text.x = element_text(angle = 45,hjust = 1))
#
#
