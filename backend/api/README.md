# API Testing

## Installation

Create a virtual environment of your choosing. Ths guide uses conda.

```
conda create --name skillset python=3.11
conda activate skillset
```

Install the required packages as listed in `requirements.txt`

```
cd backend
pip3 install -r requirements.txt
```

Register an osu! OAuth application by following the instructions [here](https://osu.ppy.sh/docs/index.html#registering-an-oauth-application). The callback URL does not matter, as we authenticate through the Client Credentials grant, meaning we do not need to "be" a user.

Create a `.env` file:

```
cp .env.EXAMPLE .env
```

In the `.env` file, enter your Client ID and Secret.
