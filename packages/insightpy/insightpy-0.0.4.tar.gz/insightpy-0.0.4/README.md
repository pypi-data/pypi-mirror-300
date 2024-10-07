# InsightPy

![License](https://img.shields.io/github/license/habib-z/insightpy)
![PyPI Version](https://img.shields.io/pypi/v/insightpy)
![Python Versions](https://img.shields.io/pypi/pyversions/insightpy)
![PyPI Downloads](https://img.shields.io/pypi/dm/insightpy)
![Code Coverage](https://codecov.io/gh/habib-z/insightpy/branch/main/graph/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/habib-z/insightpy)
![Contributors](https://img.shields.io/github/contributors/habib-z/insightpy)
![Issues](https://img.shields.io/github/issues/habib-z/insightpy)
![Repo Size](https://img.shields.io/github/repo-size/habib-z/insightpy)
![Commits Per Month](https://img.shields.io/github/commit-activity/m/habib-z/insightpy)
![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)
[![Work in Progress](https://img.shields.io/badge/status-in%20development-orange.svg)](https://github.com/your-repo)

[//]: # (![Build]&#40;https://img.shields.io/github/actions/workflow/status/habib-z/insightpy/ci.yml?branch=main&#41;)

```markdown
 ⚠️ Notice: Project Under Development
```
**InsightPy is currently in development and not ready for production use. Please avoid installing or using it until a stable version is released.**

## Data Profiler
This is a data profiling tool that provides quick insights into your dataset.

### Features:
- Summary statistics (mean, median, standard deviation)
- Missing value analysis
- Recommend Different transformation and Encoding and feature interaction based on various statistical analysis 
- Correlation analysis
- Histogram and scatter plot visualizations

### Installation:
```bash
pip install insightpy
```

### Usage:
```python
df=pd.read_csv("./data.csv")
insightpy.analyze(df,column_name)
```

More features and UI will be added soon!
