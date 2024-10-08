"""
Exploratory Data Analysis (EDA) Module
--------------------------------------
해당 모듈은 데이터셋에 대한 EDA 분석을 수행하는 모듈입니다.
Documentation 및 예시로 작성해둔 Jupyter Notebook 파일을 참고하여 분석을 진행하시면 됩니다.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
from scipy.interpolate import make_interp_spline
import squarify
from math import pi
import plotly.graph_objects as go
from matplotlib import cm

def auto_eda(data, report_path='auto_eda_report.html'):
    """
    sweetviz를 활용한 Auto EDA 리포트를 html로 생성

    Args:
        data (pd.DataFrame): EDA를 수행할 입력 데이터.
        report_path (str, optional): 생성된 리포트를 저장할 파일 경로.

    Returns:
        None
    """
    import sweetviz as sv

    # Sweetviz Auto EDA 분석 수행
    report = sv.analyze(data)

    # 리포트를 HTML 파일로 저장
    report.show_html(filepath=report_path)

def auto_eda_comparison(data1, data2, report_path='auto_eda_comparison_report.html'):
    """
    sweetviz를 활용한 Auto EDA 비교 리포트(ex. 데이터프레임의 sub segment)를 html로 생성

    Args:
        data1 (pd.DataFrame): 비교할 첫 번째 데이터프레임.
        data2 (pd.DataFrame): 비교할 두 번째 데이터프레임.
        report_path (str, optional): 생성된 리포트를 저장할 파일 경로.

    Returns:
        None
    """
    import sweetviz as sv

    # Sweetviz EDA 비교 리포트 생성
    report = sv.compare([data1, "Data1"], [data2, "Data2"])

    # 리포트를 HTML 파일로 저장
    report.show_html(filepath=report_path)

# Standard Chartered colors
SC_COLORS = ['#38d200', '#0473ea', '#525355', '#0061c7']

def plot_pie_chart(df: pd.DataFrame, label_column: str, size_column: str = None, colors: list = SC_COLORS, title: str = "Pie Chart") -> None:
    """
    Pie chart 그리기

    Args:
        df: DataFrame.
        label_column: Label 컬럼.
        size_column: Size 컬럼.
        colors: 색상 리스트.
        title: 차트 제목.
    """
    sizes = df[size_column] if size_column else df[label_column].value_counts()
    labels = df[label_column].unique()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')
    plt.title(title)
    plt.show()

def plot_grouped_donut_pie_chart(df: pd.DataFrame, group_column: str, value_column: str, colors: list = SC_COLORS, title_prefix: str = "Distribution for") -> None:
    """
    Grouped donut pie chart 그리기

    Args:
        df: DataFrame.
        group_column: Group 컬럼.
        value_column: Value 컬럼.
        colors: 색상 리스트.
        title_prefix: 차트 제목 Prefix.
    """
    groups = df[group_column].unique()
    for group in groups:
        group_data = df[df[group_column] == group]
        value_counts = group_data[value_column].value_counts().sort_index()

        labels = value_counts.index
        sizes = value_counts.values

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plt.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.title(f'{title_prefix} {group}')
        plt.show()

def plot_stacked_column_chart(df: pd.DataFrame, category_column: str, stack_column: str, colors: list = SC_COLORS) -> None:
    """
    Stacked column chart 그리기

    Args:
        df: DataFrame.
        category_column: Category 컬럼.
        stack_column: Stack 컬럼.
        colors: 색상 리스트.
    """
    cross_tab = pd.crosstab(df[category_column], df[stack_column])
    cross_tab.plot(kind='bar', stacked=True, figsize=(10, 6), color=colors)
    plt.xlabel(category_column)
    plt.ylabel('Count')
    plt.legend(title=stack_column, loc='upper right')
    plt.show()

def plot_heatmap(df: pd.DataFrame, color: str = SC_COLORS[1]) -> None:
    """
    Heatmap 그리기

    Args:
        df: DataFrame.
        color: 색상.
    """
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr_matrix = numeric_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap=color, linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()

def plot_treemap(df: pd.DataFrame, size_column: str, label_column: str, color: str = SC_COLORS[1]) -> None:
    """
    Treemap 그리기

    Args:
        df: DataFrame.
        size_column: Size 컬럼.
        label_column: Label 컬럼.
        color: 색상.
    """
    sizes = df[size_column]
    labels = df[label_column]
    sizes = sizes[sizes > 0]
    labels = labels[sizes.index]
    cmap = cm.get_cmap(color)
    colors = cmap(sizes / max(sizes))

    plt.figure(figsize=(10, 6))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8)
    plt.title(f'Treemap of {label_column} by {size_column}')
    plt.axis('off')
    plt.show()

def plot_trend_line_chart(df: pd.DataFrame, x_column: str, y_column: str, title: str, x_label: str, y_label: str, color: str = SC_COLORS[1]) -> None:
    """
    Trend line chart 그리기

    Args:
        df: DataFrame.
        x_column: X 축.
        y_column: Y 축.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        color: 색상.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_column], df[y_column], color=color, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

def plot_multi_line_chart(df: pd.DataFrame, x_column: str, y_columns: list, title: str, x_label: str, y_label: str, colors: list = SC_COLORS) -> None:
    """
    Multi-line chart 그리기

    Args:
        df: DataFrame.
        x_column: X 축.
        y_columns: Y 축 리스트.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        colors: 색상 리스트.
    """
    plt.figure(figsize=(10, 6))
    for i, y_column in enumerate(y_columns):
        plt.plot(df[x_column], df[y_column], label=y_column, color=colors[i])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(title="Legend", loc="best")
    plt.grid(True)
    plt.show()

def plot_area_chart(df: pd.DataFrame, x_column: str, y_column: str, title: str, x_label: str, y_label: str, alpha: float = 0.6, color: str = SC_COLORS[1]) -> None:
    """
    Area chart 그리기

    Args:
        df: DataFrame.
        x_column: X 축.
        y_column: Y 축.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        alpha: 투명도.
        color: 색상.
    """
    plt.figure(figsize=(10, 6))
    plt.fill_between(df[x_column], df[y_column], color=color, alpha=alpha)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

def plot_stacked_area_chart(df: pd.DataFrame, x_column: str, y_columns: list, title: str, x_label: str, y_label: str, alpha: float = 0.6, colors: list = SC_COLORS) -> None:
    """
    Stacked area chart 그리기

    Args:
        df: DataFrame.
        x_column: X 축.
        y_columns: Y 축 리스트.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        alpha: 투명도.
        colors: 색상 리스트.
    """
    plt.figure(figsize=(10, 6))
    plt.stackplot(df[x_column], df[y_columns].T, labels=y_columns, colors=colors, alpha=alpha)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc="upper left", title="Legend")
    plt.grid(True)
    plt.show()

def plot_spline_chart(df: pd.DataFrame, x_column: str, y_column: str, title: str, x_label: str, y_label: str, color: str = SC_COLORS[1]) -> None:
    """
    Spline chart 그리기

    Args:
        df: DataFrame.
        x_column: X 축.
        y_column: Y 축.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        color: 색상.
    """
    x = df[x_column]
    y = df[y_column]
    x_new = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_smooth = spline(x_new)

    plt.figure(figsize=(10, 6))
    plt.plot(x_new, y_smooth, color=color)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

def plot_single_value_card(value: float, title: str, subtitle: str = None, font_size: int = 24, subtitle_size: int = 16, color: str = SC_COLORS[0]) -> None:
    """
    Single value card 그리기

    Args:
        value: 표시할 값.
        title: 카드 제목.
        subtitle: 부제목.
        font_size: 폰트 크기.
        subtitle_size: 부제목 폰트 크기.
        color: 배경색.
    """
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_facecolor(color)

    plt.text(0.5, 0.6, f"{value:,}", ha='center', va='center', fontsize=font_size, color="black", weight='bold', transform=ax.transAxes)
    plt.text(0.5, 0.85, title, ha='center', va='center', fontsize=subtitle_size, color="black", transform=ax.transAxes)

    if subtitle:
        plt.text(0.5, 0.3, subtitle, ha='center', va='center', fontsize=subtitle_size, color="black", transform=ax.transAxes)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.show()

def plot_table_chart(df: pd.DataFrame, title: str, col_width: float = 0.2, row_height: float = 0.4, font_size: int = 12, header_color: str = SC_COLORS[1], row_colors: list = [SC_COLORS[2], SC_COLORS[3]], edge_color: str = 'black') -> None:
    """
    Table chart 그리기

    Args:
        df: DataFrame.
        title: 테이블 제목.
        col_width: 컬럼 너비.
        row_height: 행 높이.
        font_size: 폰트 크기.
        header_color: 헤더 색상.
        row_colors: 행 색상 리스트.
        edge_color: 테두리 색상.
    """
    fig, ax = plt.subplots(figsize=(len(df.columns) * col_width, len(df) * row_height))
    ax.set_title(title, fontdict={'fontsize': font_size + 2}, loc='center')

    table_data = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colWidths=[col_width] * len(df.columns))
    table_data.auto_set_font_size(False)
    table_data.set_fontsize(font_size)
    table_data.scale(1.2, 1.2)

    for key, cell in table_data.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[key[0] % len(row_colors)])
        cell.set_edgecolor(edge_color)

    ax.axis('tight')
    ax.axis('off')
    plt.tight_layout()
    plt.show()

def plot_histogram(df: pd.DataFrame, column: str, bins: int, title: str, x_label: str, y_label: str, color: str = SC_COLORS[1]) -> None:
    """
    Histogram 그리기

    Args:
        df: DataFrame.
        column: 히스토그램 컬럼.
        bins: bin 개수.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        color: 색상.
    """
    plt.figure(figsize=(8, 6))
    plt.hist(df[column], bins=bins, color=color, edgecolor='black')
    plt.title(title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True)
    plt.show()

def plot_box_plot(df: pd.DataFrame, column: str, title: str, y_label: str, color: str = SC_COLORS[2]) -> None:
    """
    Box plot 그리기

    Args:
        df: DataFrame.
        column: Box plot 컬럼.
        title: 차트 제목.
        y_label: Y 축 레이블.
        color: 색상.
    """
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, y=column, color=color)
    plt.title(title, fontsize=16)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True)
    plt.show()

def plot_violin_plot(df: pd.DataFrame, x_column: str, y_column: str, title: str, x_label: str, y_label: str, color: str = SC_COLORS[1]) -> None:
    """
    Violin plot 그리기

    Args:
        df: DataFrame.
        x_column: X 축.
        y_column: Y 축.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        color: 색상.
    """
    plt.figure(figsize=(8, 6))
    sns.violinplot(data=df, x=x_column, y=y_column, color=color)
    plt.title(title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True)
    plt.show()

def plot_density_plot(df: pd.DataFrame, column: str, hue: str = None, shade: bool = True, title: str = "Density Plot", x_label: str = "", y_label: str = "", color: str = SC_COLORS[0]) -> None:
    """
    Density plot 그리기

    Args:
        df: DataFrame.
        column: Density 컬럼.
        hue: Hue.
        shade: 음영 처리 여부.
        title: 차트 제목.
        x_label: X 축 레이블.
        y_label: Y 축 레이블.
        color: 색상.
    """
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x=column, hue=hue, shade=shade, color=color)
    plt.title(title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True)
    plt.show()
