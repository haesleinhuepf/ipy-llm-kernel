from metakernel import MetaKernel
import sys, os

DEFAULT_MODEL = "gpt-4o-2024-08-06"

llm_name = os.environ.get("IPY_LLM_KERNEL_MODEL", DEFAULT_MODEL)

class LLMKernel(MetaKernel):
    implementation = 'llm-kernel'
    implementation_version = '1.1'
    language = 'prompt'
    language_version = '0.1'
    banner = "llm-kernel"

    language_info = {
        'mimetype': 'text/x-prompt',
        'name': 'prompt',
        'codemirror_mode': {'name': 'prompt'},
    }

    kernel_json = {
        "argv": [sys.executable,
                 "-m", "ipy_llm_kernel",
                 "-f", "{connection_file}"],
        "display_name": f"LLM Kernel ({llm_name})",
        "language": "prompt",
        "codemirror_mode": "prompt",
        "name": f"LLM-Kernel",
        "logo": str(os.path.abspath(__file__)) + "/images/logo-64x64.png"
    }

    magic_prefixes = dict(magic='%', shell='!', help='?')
    help_suffix = "?"

    def __init__(self, *args, **kwargs):
        super(LLMKernel, self).__init__(*args, **kwargs)
        from ._endpoints import prompt_chatgpt, prompt_ollama, prompt_blablador, prompt_claude
        from functools import partial

        if "claude" in llm_name:
            self._prompt_function = partial(prompt_claude, model=llm_name)
        elif "gpt" in llm_name:
            self._prompt_function = partial(prompt_chatgpt, model=llm_name)
        elif llm_name.startswith("blablador:"):
            self._prompt_function = partial(prompt_blablador, model=llm_name)
        else:
            self._prompt_function = partial(prompt_ollama, model=llm_name)

    def get_usage(self):
        return """
        Use human language to prompt for tasks interacting with data.
        Documentation: https://github.com/haesleinhuepf/ipy-llm-kernel
        """

    def custom_display(self, obj):
        """This function makes sure that image and text output are shown properly."""
        import stackview
        if hasattr(obj, "shape") and hasattr(obj, "dtype"):
            self.Display(stackview.insight(obj))
        else:
            self.Display(obj)

    def custom_plt_show(self):
        """This function makes sure the output of matplotlib gets shown properly."""
        from stackview._static_view import _plt_to_png, _png_to_html
        from IPython.core.display import HTML
        html = _png_to_html(_plt_to_png())
        self.custom_display(HTML(html))

    def do_execute_direct(self, message):
        """This function is called when the user executes a cell with a given prompt."""
        from ._endpoints import prompt_with_memory
        from IPython.display import Markdown

        response = prompt_with_memory(message, self._prompt_function)

        self.Display(Markdown(response))

        return None

    def get_completions(self, info):
        """Auto-completion. Todo: Fill with useful content"""
        token = info["help_obj"]
        return [token + " is great. Explain why", token + " is bad. Explain why"]

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        """This function is called when a code block ends with ? We forward this to a normal cell execution"""
        expr = info["code"]
        if none_on_fail:
            return None
        else:
            return self.do_execute_direct(expr)

    # not sure if those are strictly necessary: They were added by the IDE
    def do_clear(self):
        self.Print("Clear")
        pass

    def do_apply(self, content, bufs, msg_id, reply_metadata):
        self.Print("Apply")
        pass

    async def do_debug_request(self, msg):
        self.Print("Debug")
        pass
