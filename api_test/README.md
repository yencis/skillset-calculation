# API Testing

## Installation

Create a virtual environment of your choosing. Ths guide uses conda.

```
conda create --name skillset python=3.11
conda activate skillset
```

Install the required packages as listed in `requirements.txt`

```
pip install -r requirements.txt
```

Register an osu! OAuth application by following the instructions [here](https://osu.ppy.sh/docs/index.html#registering-an-oauth-application).

Create a `.env` file:

```
cp .env.EXAMPLE .env
```

In the `.env` file, enter your Client ID and Secret.
