import os
class SolveCaptcha:
    def __init__(self, page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None

    def delay(self):
        self.page.wait_for_timeout(random.randint(1, 3) * 1000)

    def presetup(self):
        name = self.page.locator(
            "//iframe[@title='reCAPTCHA']").get_attribute("name")
        self.recaptcha = self.page.frame(name=name)

        self.recaptcha.click("//div[@class='recaptcha-checkbox-border']")
        self.delay()
        s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
        if s.get_attribute("aria-checked") != "false":  # solved already
            return

        self.main_frame = self.page.frame(name=page.locator(
            "//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute("name"))
        self.main_frame.click("id=recaptcha-audio-button")

    def start(self):
        self.presetup()
        tries = 0
        while (tries <= 5):
            self.delay()
            try:
                self.solve_captcha()
            except Exception as e:
                print(e)
                self.main_frame.click("id=recaptcha-reload-button")
            else:
                s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
                if s.get_attribute("aria-checked") != "false":
                    self.page.click("id=recaptcha-demo-submit")
                    self.delay()
                    break
            tries += 1

    def solve_captcha(self):
        self.main_frame.click(
            "//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = self.main_frame.locator(
            "//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")

        urllib.request.urlretrieve(href, "audio.mp3")

        sound = pydub.AudioSegment.from_mp3(
            "audio.mp3").export("audio.wav", format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(text)
        self.main_frame.fill("id=audio-response", text)
        self.main_frame.click("id=recaptcha-verify-button")
        self.delay()

    def __del__(self):
        os.remove("audio.mp3")
        os.remove("audio.wav")
