# ISAC 教材项目结构与协作规范

本项目旨在完成《Integrated Sensing and Communication: Theory and Applications》教材初稿，并在多人协作过程中统一章节结构、标题层级、图表风格、参考文献格式和编译方式。

## 1. 项目目录结构

请在对应目录中维护相关内容，不要随意调整全书主控文件和公共配置。

```text
ISAC-Draft/
├── main.tex                 # 全书主控文件：宏包、页面格式、目录、章节入口、参考文献入口
├── chapters/                # 正文章节
│   ├── acronyms.tex          # 全书缩略语表
│   └── chapter1/
│       ├── chapter1.tex      # Chapter 1 的章节入口文件
│       ├── sec1_en.tex       # Chapter 1 Section 1
│       ├── sec2_en.tex       # Chapter 1 Section 2
│       ├── sec3.tex          # Chapter 1 Section 3
│       └── exercises/        # Chapter 1 各 section 的习题文件
├── figures/                 # 全书图像文件
│   └── chapter1/             # Chapter 1 使用的图像
├── code/                    # 生成图片或仿真结果的代码
│   └── chapter1/             # Chapter 1 对应代码
├── bib/
│   └── references.bib        # 全书参考文献数据库
├── appendix/                # 附录
├── backmatter/              # 书末内容，如配套代码说明、习题答案
│   └── exercise_solutions/   # 按 chapter/sec 管理的习题答案
└── Readme.md                # 项目结构与协作规范
```

LaTeX 编译产物，例如 `.aux`、`.bbl`、`.blg`、`.log`、`.out`、`.toc`、`.synctex.gz`、`.xdv`、`main.pdf` 等，不需要手动修改，也不应作为正文文件提交。

## 2. 正文章节组织

全书由 `main.tex` 统一控制。每一章在 `chapters/chapterX/` 下维护，章入口文件负责组织本章各节内容。

例如 Chapter 1 的入口文件是：

```latex
\chapter{...}
\input{chapters/chapter1/sec1_en}
\input{chapters/chapter1/sec2_en}
\input{chapters/chapter1/sec3}
\input{chapters/chapter1/exercises/sec1_en_exercises}
\input{chapters/chapter1/exercises/sec2_en_exercises}
\input{chapters/chapter1/exercises/sec3_exercises}
```

协作者通常只需要修改自己负责的 `secX.tex` 文件。除非需要新增章节、调整全书宏包、修改页面样式或改变全书编译方式，否则不应改动 `main.tex`。

## 3. 习题与答案管理

习题和答案也按 `chapter/sec` 分文件管理，避免多人协作时把所有题目或答案写在同一个文件里。

正文习题文件放在对应章节的 `exercises/` 目录下，例如：

```text
chapters/chapter1/exercises/sec1_en_exercises.tex
chapters/chapter1/exercises/sec2_en_exercises.tex
chapters/chapter1/exercises/sec3_exercises.tex
chapters/chapter2/exercises/sec1_exercises.tex
```

各章入口文件负责 `\input{...}` 对应习题文件。若某个 section 暂时没有习题，可以保留空的占位文件，只写注释，不生成任何正文内容。

建议习题文件使用下面的基本格式：

```latex
\section*{Exercises}
\addcontentsline{toc}{section}{Exercises}

\begin{enumerate}[label=\textbf{Exercise 1.\arabic*.}, leftmargin=*]
    \item ...
\end{enumerate}
```

书末答案放在 `backmatter/exercise_solutions/` 下，并继续按 `chapter/sec` 拆分，例如：

```text
backmatter/exercise_solutions/exercise_solutions.tex
backmatter/exercise_solutions/chapter1/sec1_en_solutions.tex
backmatter/exercise_solutions/chapter1/sec2_en_solutions.tex
backmatter/exercise_solutions/chapter1/sec3_solutions.tex
backmatter/exercise_solutions/chapter2/sec1_solutions.tex
```

其中 `backmatter/exercise_solutions/exercise_solutions.tex` 只作为答案总入口，负责 `\input{...}` 各 section 的答案文件。具体答案应写在各自负责 section 的 `secX_solutions.tex` 文件中。

建议答案文件使用下面的基本格式：

```latex
\section*{Chapter 1: Introduction}
\addcontentsline{toc}{section}{Chapter 1: Introduction}

\subsection*{Section 1.1 Exercises}

\begin{enumerate}[label=\textbf{Exercise 1.\arabic*.}, leftmargin=*]
    \item ...
\end{enumerate}
```

新增习题时，应同时新增或更新对应答案文件，并保持题目编号和答案编号一致。

## 4. 标题层级规范

本项目使用下面的标题层级。标题层级不要随意跳级。

```latex
\chapter{Chapter Title}
\section[Short Title for ToC and Header]{Full Section Title}
\subsection{Subsection Title}
\subsubsection{Subsubsection Title}
```

其中，`\section[短标题]{正文标题}` 的方括号内容用于目录和页眉，花括号内容用于正文显示。当正文标题较长时，应设置简洁短标题，避免目录和页眉过长。

节内还定义了两个项目专用标题命令：

```latex
\topichead{Low-Altitude Economy and UAV Scenarios}

Low-altitude economy and UAV scenarios usually involve UAV control,
task data transmission, airspace monitoring, and multi-UAV cooperation.
```

排版效果：`\topichead{}` 会形成独立的加粗主题块标题，标题单独占一行，后续正文另起一段。它适合用于 section 内部的场景分类、概念分类或并列主题。

```latex
\runinhead{Frequency-modulated continuous-wave radar.}
FMCW radar transmits a chirp signal whose instantaneous frequency changes
with time.
```

排版效果：`\runinhead{}` 会形成段首嵌入式加粗小标题，标题和正文在同一段中连续排版。它适合用于短定义、短说明或段落内部的局部主题，例如 FMCW radar、CW radar、pulse radar 这类紧凑说明。

使用建议：

- `\section{}` 和 `\subsection{}` 用于正式目录结构。
- `\topichead{}` 用于节内较明显的主题块，但不进入目录。
- `\runinhead{}` 用于段落级提示，不进入目录。
- 不要为了视觉效果随意使用 `\\` 强制换行；标题过长时，应优先使用短标题，必要时再在标题内部谨慎加入手动换行。

## 5. 图表规范

图像统一放在 `figures/chapterX/` 下。若图像由仿真、数据处理或绘图脚本生成，对应脚本应放在 `code/chapterX/` 下。

插图使用下面的基本格式：

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/chapter1/figure_name.png}
    \caption{Caption text.}
    \label{fig:figure-name}
\end{figure}
```

表格使用三线表风格，避免竖线：

```latex
\begin{table}[htbp]
    \centering
    \caption{Caption text.}
    \label{tab:table-name}
    \begin{tabular}{lll}
        \toprule
        Column 1 & Column 2 & Column 3 \\
        \midrule
        A & B & C \\
        \bottomrule
    \end{tabular}
\end{table}
```

图题放在图像下方，表题放在表格上方。正文中引用图表时使用 `Fig.~\ref{fig:...}`、`Table~\ref{tab:...}`，不要手写编号。

## 6. 缩略语与参考文献

全书缩略语统一维护在 `chapters/acronyms.tex`。正文中优先使用项目已有的缩略语命令，例如：

```latex
\ac{ISAC}
\acs{WLAN}
```

参考文献统一维护在 `bib/references.bib`。正文引用使用：

```latex
... as described in recent standardization documents~\cite{ITU_M2160_2023}.
```

本项目采用 IEEE 数字编号引用风格，`main.tex` 中使用：

```latex
\bibliographystyle{IEEEtran}
\bibliography{bib/references}
```

新增标准、技术报告或网页类引用时，应尽量包含机构作者、标题、机构、类型、编号、年份、官方 URL 和访问日期等信息。

## 7. 编译方式

本项目使用 `fontspec`，需要使用 XeLaTeX 编译。推荐完整编译顺序为：

```text
XeLaTeX -> BibTeX -> XeLaTeX -> XeLaTeX
```

如果使用 VS Code 或命令行，也可以使用 `latexmk` 自动完成多轮编译。编译后重点检查：

- 目录、图表编号和公式编号是否更新；
- 参考文献是否正常显示；
- 缩略语是否正常链接；
- 是否存在明显的 overfull/underfull 排版警告。

## 8. 协作规则

- 只修改自己负责的章节文件，公共文件改动需要提前说明。
- 习题和答案应分别写入自己负责 section 对应的 `exercises/` 和 `exercise_solutions/` 文件，不要集中写入章入口文件或答案总入口。
- 新增图像时，应将图像文件放入对应章节的 `figures/chapterX/` 目录。
- 新增由代码生成的图像时，应同时提交对应的 `code/chapterX/` 脚本。
- 新增参考文献时，应写入 `bib/references.bib`，并在正文中使用 `\cite{...}` 引用。
- 新增缩略语时，应写入 `chapters/acronyms.tex`，避免同一缩略语在不同章节重复定义。
- 不提交 LaTeX 编译产物和临时审阅文件。
- 专业术语、章节标题、场景分类和核心技术分类发生变化时，应先与作者确认。
