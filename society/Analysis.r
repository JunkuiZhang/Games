library(ggplot2)

world_data <- read.csv("./Data/test0.csv", header = T)
qplot(x = Time, y = Gini, data = world_data, geom = "line") + 
      labs(title = "The Richest Entity's Welfare")

entity_data <- read.csv("./Data/test1.csv", header = T)
ggplot(data = entity_data, aes(x = Time, group = factor(ID))) + 
      geom_line(aes(y = Welfare, color = factor(ID))) + 
      geom_line(aes(y = Threshold), size = 0.5)

qplot(data = entity_data, x = Field_product, geom = "histogram") + 
      geom_vline(xintercept = mean(entity_data[entity_data$Time == 1,]$Field_product), size = 0.5) + 
      labs(title = "Barplot of Field Production", x = "Field production", y = "Count")