from tqdm import tqdm


class ProgressBar:
    def __init__(self, total: int, desc: str = "Progress"):
        """
        Initializes the progress bar.

        Args:
            total (int): The total number of steps for the progress bar.
            desc (str): A description label for the progress bar.
        """
        self.total = total
        self.progress = 0
        self.bar = tqdm(total=self.total, desc=desc, leave=True, position=0)

    def set_progress(self, value: int):
        """
        Sets the progress bar to a specific value.

        Args:
            value (int): The current progress value to set the bar to.
        """
        if 0 <= value <= self.total:
            self.bar.n = value
            self.bar.refresh()
            self.progress = value
        else:
            raise ValueError(f"Value must be between 0 and {self.total}")

    def update(self, increment: int = 1):
        """
        Increments the progress bar by a specific amount.

        Args:
            increment (int): The amount to increment the progress bar by. Default is 1.
        """
        self.bar.update(increment)
        self.progress += increment

    def get_progress(self) -> int:
        """
        Returns the current progress value.

        Returns:
            int: The current progress value.
        """
        return self.progress

    def set_description(self, desc: str):
        """
        Sets the description label for the progress bar.

        Args:
            desc (str): The new description label for the progress bar.
        """
        self.bar.set_description(desc)

    def get_description(self) -> str:
        """
        Returns the current description label of the progress bar.

        Returns:
            str: The current description label.
        """
        return self.bar.desc

    def close(self):
        """
        Closes the progress bar.
        """
        self.bar.close()
