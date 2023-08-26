library(tidyverse)
library(gapminder)
library(ggplot2)

head(gapminder,n=4)

gapminder %>% ggplot(aes(x=continent,y=lifeExp,fill=continent)) +
  geom_boxplot() 

gapminder %>% ggplot(aes(x=continent,y=lifeExp,fill=continent)) +
  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2)

gapminder %>% 
  mutate(yrange = c("<1980","<2000",">2000")[findInterval(gapminder$year,c(0,1980,2000,3000),all.inside = T)] ) %>% 
  ggplot(aes(x=continent,y=lifeExp,fill=factor(yrange))) + geom_boxplot()

gapminder %>% 
  mutate(yrange = c("<1980","<2000",">2000")[findInterval(gapminder$year,c(0,1980,2000,3000),all.inside = T)] ) %>% 
  ggplot(aes(x=continent,y=lifeExp,fill=factor(yrange))) + geom_boxplot() +
  labs(fill = "Year") + 
  geom_point(position = position_jitterdodge(),alpha=0.3) +
  theme_bw(base_size = 16)


gapminder %>%
  ggplot(aes(x=continent,y=lifeExp,fill=continent)) +
  geom_boxplot() + geom_jitter(width = 0.1,alpha = 0.2) +
  facet_wrap(~year) +
  theme(axis.text.x = element_text(angle = 45,hjust = 1))