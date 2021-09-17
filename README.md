# **Nine Level Data Downloader**
Downloading the nine-level teaching materials from the website [族語e樂園](http://web.klokah.tw/ninew/learn.php).
 

## **Documentation**

### 1. Import the package.

``` python
from ninelevel import NineLevel
```

If you are working on Jupyter Notebook, you need to add two additional code lines (before or after importing the `NTUACC` package):

``` python
import nest_asyncio
nest_asyncio.apply()
```
Since `NineLevel` is built with Python asynchronous frameworks, it cannot run properly on Jupyter Notebook due to the fact that Jupyter [(IPython ≥ 7.0)](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7) is already running an event loop. Visit [this question](https://stackoverflow.com/questions/56154176/runtimeerror-asyncio-run-cannot-be-called-from-a-running-event-loop) asked in StackOverflow for further details.


### 2. Select a dialect.
If you don't know which dialect's data you want to download, you can import an additional class `NineLevelDialect`:  

``` python
from ninelevel import NineLevel, NineLevelDialect
```
Use the method `.get_info()` on `NineLevelDialect` to get all the information:
- To get information of dialects:

    ```python
    NineLevelDialect.get_info()
    ```
    This prints:
    ```python
    ['卡那卡那富語',
     '撒奇萊雅語',
     '雅美語',
     '南王卑南語',
     '知本卑南語',
     '西群卑南語',
     '建和卑南語',
     '鄒語',
     ...]
    ``` 
    
### 3. Fill in and instantiate `NineLevel` class: 
#### Parameters:
* `dialect_ch`: the chinese name of the dialect  
* `level_id`: the level 
* `class_id`: the class


#### Examples:
- Select a particular level and class:

    Specify the parameter `level_id` and `class_id`: 

    ```python
    NineLevel('汶水泰雅語', level_id=1, class_id=1)
    ```
     
- Select a particular level:
    
    Specify the parameter `level_id`: 

    ```python
    NineLevel('汶水泰雅語', level_id=1)
    ```
    Without specifing the parameter `class_id`, the data will include all the nine level classes in the selected level.  

      
- Select all the levels and classes:
    
    ```python
    NineLevel('汶水泰雅語')
    ```
### 4. Print out the data: 
After filling in and instantiating the `NineLevel` class, you can use the method `.download_data()` to download the data. For example:

```python
NineLevel('汶水泰雅語', level_id=1, class_id=1).download_data()
```
This prints:
```python
{
    'level_id': '1',
    'class_id': '1',
    'title': 'lawkah su’ quw? 您好嗎？',
    'data': [
        {
            'order': '1',
            'dialect': 'papasibaq lawkah su’ quw?',
            'chinese_translation': '老師，你好嗎？'}
        }, 
        ...
    ]
}
```

### 4. Write object to a JSON file: 
After filling in and instantiating the `NineLevel` class, you can use the method `.to_json()` convert all the data to a JSON file.

```python
NineLevel('汶水泰雅語', level_id=1).to_json()
```

### 5. Write object to a CSV file: 
After filling in and instantiating the `NineLevel` class, you can use the method `.to_csv()` convert all the data to a comma-separated values (CSV) file.

```python
NineLevel('汶水泰雅語', level_id=1).to_csv()
```

## Contact Me
If you have any suggestion or question, please do not hesitate to email me at r07142010@g.ntu.edu.tw
