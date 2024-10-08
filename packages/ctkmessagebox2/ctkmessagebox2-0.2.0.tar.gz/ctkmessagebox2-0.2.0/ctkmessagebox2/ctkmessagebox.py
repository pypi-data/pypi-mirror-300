import customtkinter as ctk
from PIL import Image
import os


__all__ = ["showinfo", "showwarning", "showerror",
           "askquestion", "askokcancel", "askyesno",
           "askyesnocancel", "askretrycancel"]

def resource_path(relative_path) -> str:
    """ Retorna o caminho absoluto do recurso usando o caminho do arquivo atual """
    base_path = os.path.dirname(__file__)
    path = str(os.path.join(base_path, relative_path))
    return path

# constants
# icons

ERROR = resource_path("icons/error-icon.png")
INFO = resource_path("icons/info-icon.png")
QUESTION = resource_path("icons/ask-icon.png")
WARNING = resource_path("icons/alert-icon.png")
SUCCESS = resource_path("icons/ok-icon.png")

# types
ABORTRETRYIGNORE = "abortretryignore"
OK = "ok"
OKCANCEL = "okcancel"
RETRYCANCEL = "retrycancel"
YESNO = "yesno"
YESNOCANCEL = "yesnocancel"

# replies
ABORT = "abort"
RETRY = "retry"
IGNORE = "ignore"
# OK = "ok"
CANCEL = "cancel"
YES = "yes"
NO = "no"


def showinfo(master, title=None, message=None):
    """Show an info message"""
    return MessageBox(master, title, message, INFO, OK).get()


def showsuccess(master, title=None, message=None):
    """Show an info message"""
    return MessageBox(master, title, message, SUCCESS, OK).get()


def showwarning(master, title=None, message=None):
    """Show a warning message"""
    return MessageBox(master, title, message, WARNING, OK).get()


def showerror(master, title=None, message=None):
    """Show an error message"""
    return MessageBox(master, title, message, ERROR, OK).get()


def askquestion(master, title=None, message=None):
    """Ask a question"""
    return MessageBox(master, title, message, QUESTION, YESNO).get()


def askokcancel(master, title=None, message=None):
    """Ask if operation should proceed; return true if the answer is ok"""
    return MessageBox(master, title, message, QUESTION, OKCANCEL).get()


def askyesno(master, title=None, message=None):
    """Ask a question; return true if the answer is yes"""
    return MessageBox(master, title, message, QUESTION, YESNO).get()


def askyesnocancel(master, title=None, message=None):
    """Ask a question; return true if the answer is yes, None if cancelled."""
    return MessageBox(master, title, message, QUESTION, YESNOCANCEL).get()


def askretrycancel(master, title=None, message=None):
    """Ask if operation should be retried; return true if the answer is yes"""
    return MessageBox(master, title, message, WARNING, RETRYCANCEL).get()


class MessageBox(ctk.CTkToplevel):
    """A customtkinter message box"""
    def __init__(self, master, title:str, message: str, _icon:str, _type:str):
        super().__init__(master)

        n_lines = len(message) // 40
        n_lines += message.count('\n')
        self.minsize(450, 150 + 10*n_lines)

        self.title(title)
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # Layout
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        msg_frame = ctk.CTkFrame(self, fg_color='transparent')
        msg_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(20,0))

        image = ctk.CTkImage(Image.open(_icon), size=(50, 50))

        ctk.CTkLabel(msg_frame, text='', image=image).pack(side=ctk.LEFT, padx=5)

        text = ctk.CTkTextbox(msg_frame, wrap='word', fg_color='transparent', height=20)
        text.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT, padx=5)
        text.insert(0.0, message)
        text.configure(state='disabled')


        buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        buttons_frame.pack(padx=20, pady=20, anchor=ctk.CENTER)

        self.result = None

        if _type == OK:
            ctk.CTkButton(buttons_frame, text='OK', width=100, command=self._ok).pack(side=ctk.LEFT, padx=5, pady=5)
        elif _type == OKCANCEL:
            ctk.CTkButton(buttons_frame, text='OK', width=100, command=self._ok).pack(side=ctk.LEFT, padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='Cancel', width=100, command=self._no).pack(side=ctk.LEFT, padx=5, pady=5)
        elif _type == RETRYCANCEL:
            ctk.CTkButton(buttons_frame, text='Retry', width=100, command=self._ok).pack(side=ctk.LEFT,padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='Cancel', width=100, command=self._no).pack(side=ctk.LEFT, padx=5, pady=5)
        elif _type == YESNO:
            ctk.CTkButton(buttons_frame, text='Yes', width=100, command=self._ok).pack(side=ctk.LEFT, padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='No', width=100, command=self._no).pack(side=ctk.LEFT, padx=5, pady=5)
        elif _type == YESNOCANCEL:
            ctk.CTkButton(buttons_frame, text='Yes', width=100, command=self._ok).pack(side=ctk.LEFT, padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='No', width=100, command=self._no).pack(side=ctk.LEFT, padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='Cancel', width=100, command=self._cancel).pack(side=ctk.LEFT, padx=5, pady=5)
        elif _type == ABORTRETRYIGNORE:
            ctk.CTkButton(buttons_frame, text='Abort', width=100, command=self._abort).pack(side=ctk.LEFT, padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='Retry', width=100, command=self._retry).pack(side=ctk.LEFT, padx=5, pady=5)
            ctk.CTkButton(buttons_frame, text='Cancel', width=100, command=self._cancel).pack(side=ctk.LEFT, padx=5, pady=5)

        self.after(100, self._make_modal)

    def _make_modal(self):
        self.grab_set()
        self.focus_force()

    def _ok(self):
        self.result = True
        self.close()

    def _no(self):
        self.result = False
        self.close()

    def _retry(self):
        self.result = RETRY
        self.close()

    def _abort(self):
        self.result = ABORT
        self.close()

    def _cancel(self):
        self.result = CANCEL
        self.close()

    def close(self):
        self.grab_release()
        self.destroy()

    def get(self):
        self.wait_window()
        return self.result

