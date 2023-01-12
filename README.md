# Stock_pricing_project

<!--这一部分介绍背景
-------------------------------------------------------------------------------------->
## 01 Background
This assignment project can combine data from multiple CSV files into a single table, calculate individual and abnormal stock returns, and compute returns for a portfolio of stocks.

This task can be broken down into a series of intermediary steps:
* Create a data frame containing the stock price data for multiple companies.
* Calculate returns for each of these companies.
* Subtract the market returns from each individual stock returns to generate abnormal returns.
* Ccompare the performance of given companies over given period.


<!--这一部分介绍构思
-------------------------------------------------------------------------------------->
## 02 Ideas
I think there are three struct variables could be constructed to store the detailed informtion needed.
- struct land, this is to store the state of an individual block of land, contains information include:
```c
struct land {
    int is_watered;   // is this block currently watered or not.
    char seed_name;   // the single letter name of the seed currently planted in this block.
};
```
-	struct seeds, this is to store information about a single type of seed.
```c
struct seeds {
    char name;        // stores the single letter name of this type of seed.
    int amount;       // stores the number of available seeds to plant.
};
```
-	struct farmer, is to store the current state of a farmer.
```c
struct farmer {
    int curr_col;     // stores the current column coordinate of the farmer.
    int curr_row;     // stores the current row coordinate of the farmer.
    char curr_dir;    // stores a character representing the direction the farmer is currently facing, only have values of >, <, v, and ^.
};
```
Then the 

-------------------------------------------------------------------------------------->
## The Source Files
All required files are included in the archive with the following structure:/n
project2/ /n
| /n
|__ __init__.py
|__ config.py
|__ project_desc.pdf
|__ zid_project2.py
|
|___data/
| | <many csv files here>
where
• project2/ represents the main folder containing all the project files.
• zid_project2.py contains the functions you need to write for this project. This is the only file you
need to submit.
• project_desc.pdf is the PDF version of this document.
• data/: This is the sub-directory where all the data files for this files are stored. Inside this folder you
will find many files. Each <tic>_prc.csv contains stock price data for the ticker <tic>. These CSV
files include the column names in a header row of text. In addition, this folder contains a file called
ff_daily.csv, which includes market returns.
• config.py is the configuration module for this package. You do not need to modify this file.



<!--这一部分介绍项目里用到的文件 和文件里用到的函数
-------------------------------------------------------------------------------------->
## 03 Functions
### Intialization functions
This function initializes the struct farmer, seeds and the farm_land.
```c
struct farmer initialise_farmer(struct farmer cse_farmer);
void initialise_seeds(struct seeds seed_collection[MAX_NUM_SEED_TYPES]);
void initialise_land(struct land farm_land[LAND_SIZE][LAND_SIZE]);
```

### Print functions
These function is constructed to print the whole map of grids, hence provide a interface for a manipulation of the farmer's movements and actions.
print_all_seeds offers a tool for tha player to check the seeds and corresponding amounts.
```c
void print_land(struct land farm_land[LAND_SIZE][LAND_SIZE], struct farmer cse_farmer);
void print_top_row(struct land farm_land[LAND_SIZE][LAND_SIZE], int row);
void print_farmer_row(struct land farm_land[LAND_SIZE][LAND_SIZE], struct farmer cse_farmer);
static void print_all_seeds(struct seeds seed_collection[MAX_NUM_SEED_TYPES]);
```

<!--如何使用这份文件
-------------------------------------------------------------------------------------->
## 04 User Guide
There is only one script for this farming game, farmer.c. After compile this script you would get farmer. 
Run this application by input ```./farmer``` in the terminal, next, input the total number of seeds you wanna plant and the name of the types of seeds, just as the screenshot showed below.

<img width="396" alt="image" src="https://user-images.githubusercontent.com/86709726/211798346-f6c8650a-37c3-4296-a0ba-17873b60db1c.png">

By sending command a, you would get the information of the seeds set you typed in.

<img width="356" alt="image" src="https://user-images.githubusercontent.com/86709726/211798763-5312ccea-2ebe-42b3-a030-fd24a604e9fe.png">

By sending command l, you would get the whole map of the game.

<img width="216" alt="image" src="https://user-images.githubusercontent.com/86709726/211799326-072dc244-d34b-482c-a284-98d78c927dcf.png">



<!--命令表
-------------------------------------------------------------------------------------->
## 05 Table of Commands
```
Printing All Seeds              	      a
Printing Land	                              l
Moving Upwards	                              ^
Moving Right	                              > 
Moving Downwards	                      v
Moving Left	                              <
Watering an Adjacent Land	              o w
Planting on an Adjacent Land	              o p
Scattering Seeds	                      p
Watering a Square	                      w
Advancing to the Next Day	              n
Harvesting an Adjacent Plant	              h
Trading Seeds	                              t
Expriencing Droughts	                      d d
Experiencing Wind Storms	              d w
```
