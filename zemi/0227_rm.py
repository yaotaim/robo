b3_3@sirius-NUC13ANHi5:~/tanaka$ python3 0227_gpt.py 
You: hello
Traceback (most recent call last):
  File "/home/b3_3/tanaka/0227_gpt.py", line 14, in response
    response = openai.Completion.create(
  File "/home/b3_3/.local/lib/python3.10/site-packages/openai/lib/_old_api.py", line 39, in __call__
    raise APIRemovedInV1(symbol=self._symbol)
openai.lib._old_api.APIRemovedInV1: 

You tried to access openai.Completion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/b3_3/tanaka/0227_gpt.py", line 27, in <module>
    reply = chatbot.response(user_input)
  File "/home/b3_3/tanaka/0227_gpt.py", line 21, in response
    except openai.error.OpenAIError as e:
AttributeError: module 'openai' has no attribute 'error'
