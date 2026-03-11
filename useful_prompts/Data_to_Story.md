# Prompt generator

## 1. Find dataset

I am running a workshop on how to use LLM and Generative AI for data visualization. It will be having participants with mixed background - from senior executives to various level of architects. We will be doing the analysis, creating the code, all works using LLMs. 
Please suggest a few datasets which are freely available online, and something nice, interesting, thought-provoking. 
For first iteration, I would like to take something that is not too big, say approximately 100000 records max, having a reasonable variety of columns and text, long text, categories, numerical values, date etc. 
Most importantly, the story should be interesting for a wide variety of audiences. So please find few things that are cool. 


## Ideation

These are the columns in the dataset {dataset_name}: 
{columns}

I would like to create interesting stories based on this dataset that can also be visualized nicely. 
Please give me a dozen suggestions on 1) what stories to write 2) who they would be interesting to and why and 3) how we can do this step by step using a LLM 


## Analyze, Visualize

Run all of these analysis, do everything needed for statistical hypothesis testing that will be useful. Flag off things which are not statistically significant, drop those part of the analysis. 
Enrich the story with beautiful charts. Charts with matplotlib are often not so pretty, so please try to see if there can be better visualization if possible. It should be like an award winning story with attractive visualization. 


## Meta prompt to write code

I liked all of these stories that had scatter plots in them. The only issue is that there were outliers, so I would like those removed. Now, what I want you to do is give me a prompt that I will pass to an LLM along with the data set and it should write the code as HTML JavaScript in a way that I can publish on to GitHub pages. Remember that this means that we cannot have such a large data set being uploaded on to GitHub pages and users viewing it. You need to figure out some way in the prompt of telling the LLM to create these using HTML CSS JavaScript in a way that conveys the scatter plot, but without having to load the entire data set. I am ok with the page loading data of probably up to 1 or 2 megabytes. Keep that in mind, do analysis if you need to and write the prompt.

## Prompt to improve visual

Both the data visualization and story can be better, more interesting and beautiful. So please do following -
1. Imagine you are writing a story for New York Times with beautiful data visualization. Please think how you would go about it. Choose fonts, color schemes, styling and all design choices accordingly. 
2. Create a full-fledged data story. It should be like an award winning story. 
