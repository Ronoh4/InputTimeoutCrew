from crewai_tools import BaseTool
from pydantic import Field
import threading
from queue import Queue
import time
import msvcrt 

class InputTimeoutTool(BaseTool):
    name: str = "Input Timeout Tool"
    description: str = "Tool for timing human input with a timeout mechanism"
    timeout_seconds: int = Field(default=10)

    def __init__(self, timeout_seconds: int = 10):
        super().__init__(timeout_seconds=timeout_seconds)
        self.timeout_seconds = timeout_seconds

    def _get_input_with_timeout(self, prompt: str) -> tuple[bool, str]:
        user_input = Queue()
        input_started = threading.Event()
        
        def input_thread():
            try:
                print(prompt, end='', flush=True)
                buffer = []
                while True:
                    if msvcrt.kbhit():
                        if not input_started.is_set():
                            input_started.set()
                        
                        char = msvcrt.getwch()
                        if char == '\r':  # Enter key
                            print()  # New line
                            user_input.put(''.join(buffer))
                            break
                        elif char == '\b':  # Backspace
                            if buffer:
                                buffer.pop()
                                print('\b \b', end='', flush=True)
                        else:
                            buffer.append(char)
                            print(char, end='', flush=True)
            except:
                user_input.put(None)

        thread = threading.Thread(target=input_thread)
        thread.daemon = True
        thread.start()

        try:
            start_timeout = time.time()
            while not input_started.is_set():
                if time.time() - start_timeout >= self.timeout_seconds:
                    print(f"\nTimeout of {self.timeout_seconds}s reached. Automatically approving...")
                    return False, "APPROVED"
                time.sleep(0.1)
            
            result = user_input.get()
            return True, result if result is not None else ""
        except:
            print(f"\nTimeout of {self.timeout_seconds}s reached. Automatically approving...")
            return False, "APPROVED"

    def _run(self, content: str, review_type: str = "article") -> str:
        print(f"\nReviewing {review_type}:")
        print(content)
        
        prompt = (f"\nPlease review the {review_type} for accuracy.\n"
                 f"Press Enter to approve 'as is' or type your feedback [Timeout in {self.timeout_seconds}s]: ")
        
        got_input, response = self._get_input_with_timeout(prompt)
        
        if not got_input:
            return "APPROVED (automatic due to timeout)"
        elif response.strip() == "":
            return "APPROVED"
        else:
            return f"FEEDBACK: {response}"