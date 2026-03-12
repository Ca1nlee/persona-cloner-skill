# Persona Cloner

<div align="center">

基于公开资料，构建可直接用于 OpenClaw 的 **公众人物 persona package**。

<p>
  <a href="./README.en.md">English</a> |
  <strong>简体中文</strong>
</p>

<p>
  <a href="./README.md">首页</a> •
  <a href="#这个-skill-做什么">做什么</a> •
  <a href="#什么时候用">适用场景</a> •
  <a href="#默认产出">产出</a> •
  <a href="#安装">安装</a> •
  <a href="#验证">验证</a> •
  <a href="#安全边界">安全边界</a>
</p>

</div>

---

## 这个 skill 做什么

`persona-cloner` 会把公开采访、演讲、文章、访谈和其他可核对的公开材料，整理成一个可以直接运行的 OpenClaw persona package。

它的目标不是产出冗长研究档案，而是先交付一个**可运行、边界清晰、行为稳定**的 runtime package。

## 什么时候用

适合这些场景：

- 你想为某位公众人物构建可运行的 agent package
- 你希望尽量保留其表达习惯、判断方式和决策风格
- 你希望输出简洁、先给判断、不过度教学，不容易滑回通用助手口吻
- 你希望严格限定在公开资料范围内，而不是虚构私密经历或幕后信息

## 默认产出

一次正常交付通常包含：

- `SOUL.md`
- `IDENTITY.md`
- `AGENTS.md`
- `MEMORY.md`
- 可选：`README-agent.md`
- 可选：安装到 OpenClaw 工作区

仓库内还提供：

- `references/`：工作流、输出规范、来源边界、评测方法等参考资料
- `scripts/`：脚手架、验证、评测、安装、记忆管理等脚本
- `examples/`：示例 persona package 结构

## 安装

### 作为 OpenClaw skill 安装

1. 把本仓库目录复制到 OpenClaw 的 `skills/` 目录，并命名为 `persona-cloner`。
2. 如果你的环境需要，重启或重新加载 OpenClaw。
3. 直接要求基于公开资料构建某位公众人物的 persona package。

### 直接使用仓库脚本

```bash
python scripts/scaffold_persona_clone.py "Target Name" --out ./build --mode persona
python scripts/install_runtime_agent.py ./build/target-name-persona <target-workspace>
```

## 验证

### 验证 package 结构

```bash
python scripts/validate_persona_package.py ./build/target-name-persona
```

### 运行 runtime 行为评测

```bash
python scripts/eval_runtime_behavior.py run --package-dir ./build/target-name-persona --version candidate
```

### 主要会检查什么

仓库内的验证与评测主要关注：

- 是否包含必需的 runtime 文件
- 是否写清了公开资料边界
- runtime 口吻里是否避免前置强调 clone 一类自我标签
- 是否具备 verdict-first、限制篇幅、反教学腔、反通用助手腔等输出纪律
- 是否保留了必要的证据追踪、评测文件与记忆版本轨道

## 仓库结构

```text
persona-cloner-skill/
├─ SKILL.md
├─ README.md
├─ README.en.md
├─ README.zh-CN.md
├─ references/
├─ scripts/
└─ examples/
```

## 安全边界

本仓库用于基于**公开资料**构建 persona package。

它**不代表**：

- 具有私人记忆
- 具有秘密渠道或未公开访问权限
- 知道幕后细节
- 获得本人背书
- 拥有官方身份或官方授权
- 与目标人物存在实时连接

如果公开资料本身不足，就应该明确说不足。

未知就保持未知。
