import os
import random
import re


def extract_and_shuffle_problems(target_dir, output_file):
    """
    遍历 target_dir 目录中所有的 .tex 文件，提取题目，
    打乱顺序后，保存到 output_file 文件中。

    一个“题目”被定义为从 '% --- 题目 ---' 开始，
    到 '\\ansat{...}' 结束的部分。
    """

    all_problems = []
    problem_delimiter = "% --- 题目 ---"

    # 正则表达式，用于匹配 \ansat{...} 命令。
    # re.DOTALL 使得 '.' 也可以匹配换行符。
    # (?:...) 是一个非捕获组
    # [^}]* 匹配任意不是 '}' 的字符零次或多次
    ansat_regex = re.compile(r"\\ansat\{[^}]*\}", re.DOTALL)

    print(f"🚀 开始扫描目录: {target_dir}")

    for root, _, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith(".tex"):
                filepath = os.path.join(root, filename)
                print(f"  📄 正在读取文件: {filepath}")

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # 1. 使用分隔符切分文件内容
                    chunks = content.split(problem_delimiter)

                    # 2. 第一个块通常是文件头或空白，跳过 (chunks[0])
                    for chunk in chunks[1:]:
                        chunk = chunk.strip()  # 去除前后的空白
                        if not chunk:
                            continue

                        # 3. 查找 \ansat{...} 的位置
                        ansat_match = ansat_regex.search(chunk)

                        if ansat_match:
                            # 4. 提取从开头到 \ansat{...} 结尾的所有内容
                            end_index = ansat_match.end()
                            problem_block = chunk[:end_index].strip()

                            # 5. 重新组合成完整的题目（带分隔符）
                            full_problem = f"{problem_delimiter}\n{problem_block}"
                            all_problems.append(full_problem)
                        else:
                            print(
                                f"    [!] 警告: 在 {filename} 中找到一个题目块，但未找到 \\ansat :"
                            )
                            print(f"    {chunk[:70]}...")

                except Exception as e:
                    print(f"  [X] 错误: 读取或处理 {filepath} 失败: {e}")

    if not all_problems:
        print("❌ 未找到任何题目。")
        return

    print(f"\n✅ 成功提取了 {len(all_problems)} 道题目。")

    # 6. 打乱题目顺序
    random.shuffle(all_problems)
    print("🔀 题目顺序已打乱。")

    # 7. 将打乱后的题目写入新文件
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # 使用两个换行符分隔每道题，使其更易读
            f.write("\n\n".join(all_problems))
        print(f"🎉 成功将打乱后的题目写入到: {output_file}")

    except Exception as e:
        print(f"[X] 错误: 写入输出文件 {output_file} 失败: {e}")


# --- 脚本主程序 ---
if __name__ == "__main__":
    # -------------------------------------------------
    # ---           请在这里修改你的设置           ---
    # -------------------------------------------------

    # 1. 设置包含 .tex 错题文件的目标文件夹
    #    (使用正斜杠 / 作为路径分隔符)
    TARGET_DIRECTORY = "./zhenti/gailv"

    # 2. 设置输出的文件名
    OUTPUT_FILENAME = "./zhenti/gailv/GaiLvZhenTi_shuffled_problems.tex"

    # -------------------------------------------------

    # 为了方便您测试，如果目标文件夹不存在，脚本会创建一个
    if not os.path.exists(TARGET_DIRECTORY):
        print(f"目标文件夹 '{TARGET_DIRECTORY}' 不存在，将自动创建它用于测试。")
        os.makedirs(TARGET_DIRECTORY)

        # 自动创建一个基于您提供的示例内容的 .tex 文件
        dummy_content = r"""
% 这是一个自动生成的示例文件
% --- 题目 ---
\problem[P18-1 (25-2)]{设函数 $\displaystyle f(x)$ 连续, 给出下列四个条件:
\\
\textcircled{1} $\displaystyle \lim_{x \to 0} \frac{|f(x)| - f(0)}{x}$ 存在;
\\
\textcircled{2} $\displaystyle \lim_{x \to 0} \frac{f(x) - f(0)}{x}$ 存在;
\\
\textcircled{3} $\displaystyle \lim_{x \to 0} \frac{|f(x)|}{x}$ 存在;
\\
\textcircled{4} $\displaystyle \lim_{x \to 0} \frac{|f(x)| - |f(0)|}{x}$ 存在.
\\
其中能得到 “$\displaystyle f(x)$ 在 $\displaystyle x=0$ 处可导” 的条件的个数是~(~\quad~)
\begin{tasks}(4)
\task 1.
\task 2.
\task 3.
\task 4.
\end{tasks}}
\ansat{249；【十年真题】 - 考点：导数与微分的概念 - 1}

% --- 题目 ---
\problem[P18-7 (16-1)]{已知函数 $\displaystyle f(x) = \begin{cases} \displaystyle x, & \displaystyle x \le 0, \\ \displaystyle \frac{1}{n}, & \displaystyle \frac{1}{n+1} < x \le \frac{1}{n}, n = 1, 2, \dots, \end{cases}$ 则~(~\quad~)}
\begin{tasks}(2)
\task $\displaystyle x=0$ 是 $\displaystyle f(x)$ 的第一类间断点.
\task $\displaystyle x=0$ 是 $\displaystyle f(x)$ 的第二类间断点.
\task $\displaystyle f(x)$ 在 $\displaystyle x=0$ 处连续但不可导.
\task $\displaystyle f(x)$ 在 $\displaystyle x=0$ 处可导.
\end{tasks}
\ansat{250；【十年真题】 - 考点：导数与微分的概念 - 7}

% --- 题目 ---
\problem[P18-8 (25-2,3)]{设函数 $\displaystyle f(x)$ 在 $\displaystyle x = 0$ 处连续, 且 $\displaystyle \lim_{x \to 0} \frac{x f(x) - \mathrm{e}^{2\sin x} + 1}{\ln(1+x) + \ln(1-x)} = -3$, 证明 $\displaystyle f(x)$ 在 $\displaystyle x=0$ 处可导, 并求 $\displaystyle f'(0)$.}
\ansat{250；【十年真题】 - 考点：导数与微分的概念 - 8}

% --- 题目 ---
\problem[P18-9 (22-2)]{已知函数 $\displaystyle f(x)$ 在 $\displaystyle x=1$ 处可导, 且 $$\displaystyle \lim_{x \to 0} \frac{f(\mathrm{e}^{x^2}) - 3f(1 + \sin^2 x)}{x^2} = 2,$$ 求 $\displaystyle f^{\prime}(1)$.}
\ansat{250；【十年真题】 - 考点：导数与微分的概念 - 9}

% --- 题目 ---
\problem[P20-1 (07-1,2,3)]{设函数 $\displaystyle f(x)$ 在 $\displaystyle x=0$ 处连续, 下列命题错误的是~(~\quad~)
\begin{tasks}(2)
\task 若 $\displaystyle \lim_{x \to 0} \frac{f(x)}{x}$ 存在, 则 $\displaystyle f(0)=0$.
\task 若 $\displaystyle \lim_{x \to 0} \frac{f(x)+f(-x)}{x}$ 存在, 则 $\displaystyle f(0)=0$.
\task 若 $\displaystyle \lim_{x \to 0} \frac{f(x)}{x}$ 存在, 则 $\displaystyle f'(0)$ 存在.
\task 若 $\displaystyle \lim_{x \to 0} \frac{f(x)-f(-x)}{x}$ 存在, 则 $\displaystyle f'(0)$ 存在.
\end{tasks}}
\ansat{250；【真题精选】 - 考点：导数与微分的概念 - 1}

% --- 题目 ---
\problem[P20-3 (05-1,2)]{设函数 $\displaystyle f(x) = \lim_{n \to \infty} \sqrt[n]{1+|x|^{3n}}$, 则 $\displaystyle f(x)$ 在 $\displaystyle (-\infty, +\infty)$ 内~(~\quad~)}
\begin{tasks}(2)
\task 处处可导.
\task 恰有一个不可导点.
\task 恰有两个不可导点.
\task 至少有三个不可导点.
\end{tasks}
\ansat{251；【真题精选】 - 考点：导数与微分的概念 - 3}

% --- 题目 ---
\problem[P21-9 (03-3)]{设函数 $\displaystyle f(x) = \begin{cases} \displaystyle x^\lambda \cos \frac{1}{x}, & \displaystyle x \neq 0, \\ \displaystyle 0, & \displaystyle x=0, \end{cases}$ 其导函数在 $\displaystyle x=0$ 处连续, 则 $\displaystyle \lambda$ 的取值范围是 \underline{\hspace{4em}}.}
\ansat{251；【真题精选】 - 考点：导数与微分的概念 - 9}

% --- 题目 ---
\problem[P21-2 (22-2)]{已知函数 $\displaystyle y=y(x)$ 由方程
\[ x^2 + xy + y^3 = 3 \]
确定, 则 $\displaystyle y''(1) = \underline{\hspace{4em}}. $}
\ansat{251；【十年真题】 - 考点一：函数的求导与微分法则 - 2}
\vspace{12em}

% --- 题目 ---
\problem[P21-1 (21-1)]{设函数 $\displaystyle f(x)=\frac{\sin x}{1+x^2}$ 在 $\displaystyle x=0$ 处的 3 次泰勒多项式为 $\displaystyle ax+bx^2+cx^3$, 则~(~\quad~)}
\begin{tasks}(2)
\task $\displaystyle a=1, b=0, c=-\frac{7}{6}$.
\task $\displaystyle a=1, b=0, c=\frac{7}{6}$.
\task $\displaystyle a=-1, b=-1, c=-\frac{7}{6}$.
\task $\displaystyle a=-1, b=-1, c=\frac{7}{6}$.
\end{tasks}
\ansat{251；【十年真题】 - 考点二：高阶导数的计算 - 1}

% --- 题目 ---
\problem[P21-7 (16-1)]{设函数 $\displaystyle f(x) = \arctan x - \frac{x}{1+ax^2}$, 且 $\displaystyle f'''(0) = 1$, 则 $\displaystyle a = \underline{\hspace{4em}}. $}
\ansat{251；【十年真题】 - 考点二：高阶导数的计算 - 7}

% --- 题目 ---
\problem[P24-例(2)]{设函数 $\displaystyle y=x^2 \sin 2x$, 则 $\displaystyle y^{(5)}(0) = \underline{\hspace{4em}}. $}
\ansat{24；【方法探究】 - 考点二：高阶导数的计算 - 例(2)}

% --- 题目 ---
\problem[P25-7 (97-3)]{设 $\displaystyle y = f(\ln x) \mathrm{e}^{f(x)}$, 其中 $\displaystyle f$ 可微, 则 $\displaystyle \mathrm{d}y = \underline{\hspace{4em}}. $}
\ansat{252；【真题精选】 - 考点一：函数的求导与微分法则 - 7}

% --- 题目 ---
\problem[P26-2 (20-3)]{曲线 $\displaystyle x + y + \mathrm{e}^{2xy} = 0$ 在点 $\displaystyle (0, -1)$ 处的切线方程为 $\underline{\hspace{4em}}.$}
\ansat{254；【十年真题】 - 考点一：平面曲线的切线与法线 - 2}

% --- 题目 ---
\problem[P26-1 (23-2)]{设函数 $\displaystyle f(x)=(x^2+a)\mathrm{e}^x$. 若 $f(x)$ 没有极值点, 但曲线 $y=f(x)$ 有拐点, 则 $a$ 的取值范围是~(~\quad~)}
\begin{tasks}(2)
  \task $\displaystyle [0,1).$
  \task $\displaystyle [1, +\infty).$
  \task $\displaystyle [1, 2)$
  \task $\displaystyle [2, +\infty).$
\end{tasks}
\ansat{254；【十年真题】 - 考点二：利用导数判断函数的性质 - 1}

% --- 题目 ---
\problem[P26-2 (22-2)]{设函数 $\displaystyle f(x)$ 在 $\displaystyle x=x_0$ 处具有 2 阶导数, 则~(~\quad~)}
\begin{tasks}(1)
  \task 当 $\displaystyle f(x)$ 在 $\displaystyle x_0$ 的某邻域内单调增加时, $\displaystyle f'(x_0)>0$.
  \task 当 $\displaystyle f'(x_0)>0$ 时, $\displaystyle f(x)$ 在 $\displaystyle x_0$ 的某邻域内单调增加.
  \task 当 $\displaystyle f(x)$ 在 $\displaystyle x_0$ 的某邻域内是凹函数时, $\displaystyle f''(x_0)>0$.
  \task 当 $\displaystyle f''(x_0)>0$ 时, $\displaystyle f(x)$ 在 $\displaystyle x_0$ 的某邻域内是凹函数.
\end{tasks}
\ansat{254；【十年真题】 - 考点二：利用导数判断函数的性质 - 2}

% --- 题目 ---
\problem[P26-4 (19-1)]{设函数 $\displaystyle f(x)=\begin{cases} x|x|, & x \le 0, \\ x\ln x, & x > 0, \end{cases}$ 则 $\displaystyle x=0$ 是 $\displaystyle f(x)$ 的~(~\quad~)}
\begin{tasks}(2)
  \task 可导点, 极值点.
  \task 不可导点, 极值点.
  \task 可导点, 非极值点.
  \task 不可导点, 非极值点.
\end{tasks}
\ansat{254；【十年真题】 - 考点二：利用导数判断函数的性质 - 4}

% --- 题目 ---
\problem[P26-5 (16-2,3)]{设函数 $\displaystyle f(x)$ 在 $\displaystyle (-\infty, +\infty)$ 内连续, 其导函数的图形如下图所示, 则~(~\quad~)
\begin{center}
    \includegraphics[width=0.5\textwidth]{P26-5_16-2_3.png} % 
\end{center}
\begin{tasks}(1)
  \task 函数 $\displaystyle f(x)$ 有 2 个极值点, 曲线 $\displaystyle y=f(x)$ 有 2 个拐点.
  \task 函数 $\displaystyle f(x)$ 有 2 个极值点, 曲线 $\displaystyle y=f(x)$ 有 3 个拐点.
  \task 函数 $\displaystyle f(x)$ 有 3 个极值点, 曲线 $\displaystyle y=f(x)$ 有 1 个拐点.
  \task 函数 $\displaystyle f(x)$ 有 3 个极值点, 曲线 $\displaystyle y=f(x)$ 有 2 个拐点.
\end{tasks}}
\ansat{254；【十年真题】 - 考点二：利用导数判断函数的性质 - 5}

% --- 题目 ---
\problem[P26-6 (19-2,3)]{曲线 $\displaystyle y = x \sin x + 2 \cos x \ \left(-\frac{\pi}{2} < x < \frac{3\pi}{2}\right)$ 的拐点坐标为 $\underline{\hspace{4em}}.$}
\ansat{254；【十年真题】 - 考点二：利用导数判断函数的性质 - 6}

% --- 题目 ---
\problem[P26-9 (21-2)]{已知函数 $\displaystyle f(x) = \frac{x|x|}{1+x}$, 求曲线 $\displaystyle y=f(x)$ 的凹凸区间及渐近线.}
\ansat{254；【十年真题】 - 考点二：利用导数判断函数的性质 - 9}

% --- 题目 ---
\problem[P27-1 (18-3)]{设某产品的成本函数 $\displaystyle C(Q)$ 可导, 其中 $\displaystyle Q$ 为产量. 若产量为 $\displaystyle Q_0$ 时平均成本最小, 则~(~\quad~)}
\begin{tasks}(2)
  \task $\displaystyle C'(Q_0)=0$.
  \task $\displaystyle C'(Q_0)=C(Q_0)$.
  \task $\displaystyle C'(Q_0)=Q_0 C(Q_0)$.
  \task $\displaystyle Q_0 C'(Q_0)=C(Q_0)$.
\end{tasks}
\ansat{256；【十年真题】 - 考点五：导数的经济应用（仅数学三） - 1}

"""
        try:
            with open(
                os.path.join(TARGET_DIRECTORY, "example_problems.tex"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(dummy_content)
            print(f"已在 '{TARGET_DIRECTORY}' 中创建 'example_problems.tex' 供测试。")
        except Exception as e:
            print(f"创建示例文件失败: {e}")

    # 执行主函数
    extract_and_shuffle_problems(TARGET_DIRECTORY, OUTPUT_FILENAME)
