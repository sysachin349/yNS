const { chromium }  = require('playwright-extra');  // Or 'chromium' or 'webkit'.
const { exit } = require('process');
const RecaptchaPlugin = require('puppeteer-extra-plugin-recaptcha')
const fs = require('fs/promises')



const args = process.argv.slice(2)
email = args[0]
password = args[1]
proxy = args[2]
port = args[3]
longitude = args[4]
latitude = args[5]
jobid = args[6]
apikey = args[7]

chromium.use(
  RecaptchaPlugin({
    provider: {
      id: '2captcha',
      token: apikey //REPLACE THIS WITH YOUR OWN 2CAPTCHA API KEY
    },
    visualFeedback: true //colorize reCAPTCHAs (violet = detected, green = solved)
  })
)

console.log(apikey)


// y6.exe cameronlesellison0@yahoo.com yQSLLMQ1o 193.24.212.63 29842 14 22 51
async function YahooLogin( email , password , proxy , port,longitude,latitude,jobid){
    console.log(email,password,proxy,port)
    const browser = await chromium.launch({executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', headless: false ,slowMo:250, defaultViewport: null, timezone_id:"America/New_York",proxy :{'server':proxy+':'+port}});
    const context = await browser.newContext({geolocation: {"longitude": Number(longitude), "latitude": Number(latitude) }})
    const page = await context.newPage();
    page.setDefaultTimeout(10000)

    try {
        await page.goto('https://mail.yahoo.com/')
    } catch {
        await fs.writeFile('log/'+jobid+'/ProxyInternetIssue.log',email+"\n\n", { flag: 'a+' });
        process.abort()
    }
    try {
        await page.click("//a[contains(@href,'https://login.yahoo.com') and @alt='Sign in'] | //a[@name='username' and contains(@href,'https://login.yahoo.com')] | //input[@id='login-username' and @name='username']")
    } catch(e){
        //pass
    }

    // "messages.INVALID_USERNAME"
    await page.type('input[name="username"]', email)
    await delay(2000);
    console.log('USER')
    await page.click('#login-signin')
    await delay(5000);
    console.log(">> [ "+email+" ] EMAIL")
    try {
        id = await page.locator("//p[@data-error='messages.INVALID_USERNAME']").count()
        if( id > 0 ){
            console.log("INVALID USER")
            await fs.writeFile('log/'+jobid+'/InvalidEmail.log',email+"\n\n", { flag: 'a+' });
            process.abort()
        }
    } catch(e) {
        console.log(e)
    }
    // That's it, a single line of code to solve reCAPTCHAs
    await page.solveRecaptchas()
    console.log(">> [ "+email+" ] Checking For captchaFrame")
    if( await ifAvailable(page, 'iframe[src*="recaptcha/"]') ) {
        console.log(">> [ "+email+" ] Found captchaFrame... Trying To Solve")
        for (const frame of page.mainFrame().childFrames()){
            let { captchas, error }   = await frame.findRecaptchas()
            let { solutions, error1 } = await frame.getRecaptchaSolutions(captchas)
            let { solved, error2 }    = await frame.enterRecaptchaSolutions(solutions)                    
            await frame.waitForSelector('button[id="recaptcha-submit"]', { visible:true }),
            await frame.click('button[id="recaptcha-submit"]'),
            console.log("frame.click and recaptcha sloved: ")
            break;
        }
    }
    await delay(5000)
    await extraChecking(page, email,password, browser,jobid)
    await delay(5000)
    await extraChecking(page, email,password, browser,jobid)
    await delay(5000)
    await extraChecking(page, email,password, browser,jobid)
    await delay(5000)
    await extraChecking(page, email,password, browser,jobid)
    await delay(5000)
    await extraChecking(page, email,password, browser,jobid)
    await delay(5000)
    await extraChecking(page, email,password, browser,jobid)
    await delay(2000)
    process.abort()
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}


ContinueButton = async function(page,email) {
    return new Promise(async function(resolve,rejects){    
        console.log(">> [ "+email+" ] Checking For Continue Button")
        if( await ifAvailable(page, "//button[text()='Continue']")) {
            await page.click("//button[text()='Continue']")
            console.log(">> [ "+email+" ] CLICKING For Continue Button")
        }
        if( await ifAvailable(page, "//a[contains(text(),'Remind me') and contains(text(),'later')]")) {
            await page.click("//a[contains(text(),'Remind me') and contains(text(),'later')]")
            console.log(">> [ "+email+" ] CLICKING For Remind me later Button")
        }
    })
}


arkoseIframe = async function(page,email,browser,jobid) {
    return new Promise(async function(resolve,rejects){    
        console.log(">> [ "+email+" ] Checking For Arkose GAME CAPTCHA")
        if( await ifAvailable(page, "//iframe[@id='arkose-iframe']")) {
            console.log(">> [ "+email+" ] FOUND Arkose GAME CAPTCHA")
            message = "Arkose GAME CAPTCHA"
            await fs.writeFile('log/'+jobid+'/GameCaptcha.log',email+"\n\n", { flag: 'a+' });
            await delay(2000)
            process.abort()
        }
    })
}


challengeHeading = async function(page,email,browser,jobid) {
    return new Promise(async function(resolve,rejects){    
        console.log(">> [ "+email+" ] Checking For challengeHeading")
        if( await ifAvailable(page, "//h2[@class='challenge-heading']")) {
            Message = await page.locator("//h2[@class='challenge-heading']").allInnerTexts()
            if(Message == "We are unable to process your request at this time") {
                await delay(2000)
                await fs.writeFile('log/'+jobid+'/TryAfterOneHour.log',email+"\n\n", { flag: 'a+' });
                message = "Try After 1 Hour"
                process.abort()
            }
            console.log(">> [ "+email+" ] FOUND challengeHeading"+Message)
        }
    });
}


captchaFrame = async function(page, email){
    return new Promise(async function(resolve,rejects){    
        console.log(">> [ "+email+" ] Checking For captchaFrame")
        if( await ifAvailable(page, 'iframe[src*="recaptcha/"]') ) {
            console.log(">> [ "+email+" ] Found captchaFrame... Trying To Solve")
            for (const frame of page.mainFrame().childFrames()){
                let { captchas, error }   = await frame.findRecaptchas()
                let { solutions, error1 } = await frame.getRecaptchaSolutions(captchas)
                let { solved, error2 }    = await frame.enterRecaptchaSolutions(solutions)                    
                await frame.waitForSelector('button[id="recaptcha-submit"]', { visible:true }),
                await frame.click('button[id="recaptcha-submit"]'),
                console.log("frame.click and recaptcha sloved: ")
                break;
            }
        }
        await delay(5000)
    })

}


tryLogin = async function(page, email, password, browser){
    return new Promise(async function(resolve,rejects){
        console.log(">> [ "+email+" ] Checking For LOGIN INPUT")
        if( await ifAvailable(page, 'input[name="password"]')) {
            console.log(">> [ "+email+" ] FOUND LOGIN INPUT")
            await page.type('input[name="password"]', password )
            await page.click('#login-signin')

            if( await ifAvailable(page, "//button[@id='mail-accept-all-1'] | //button[@type='submit' and @name='agree' and @value='agree']") ){
                console.log(">> [ "+email+" ] Accept Policy...")
                await page.click("//button[@id='mail-accept-all-1'] | //button[@type='submit' and @name='agree' and @value='agree']")
                await delay(2000)
                await page.click("//button[@type='submit' and @name='agree']")
                await delay(3000)
            }

            if( await ifAvailable(page, "//a[@data-iskeynav='true' and contains(@href,'compose')]")) {
                await page.context().storageState({ path: "SessionData/"+email+'.json' });
                console.log(">> [ "+email+" ] LOGIN SUCCESSFULL.. SAVING STATE...")
                await delay(7000)
                if( await ifAvailable(page, "//button[@title='Done' and @data-test-id='themes-cue-done']")) {
                    await page.click("//button[@title='Done' and @data-test-id='themes-cue-done']")
                }
                await delay(2000)
            }  
            
            else {
                await page.screenshot({ path: "log/"+jobid+"/"+email+".png" });
                message = "LOGIN FAIL.. UNKNOWN ERROR.."
            }
        }
    })
}


startOver = async function(page, email, browser){
    if( await ifAvailable(page, "//button[text()='Start over']")) {
        console.log(">> [ "+email+" ] FOUND START OVER... CLOSING BROWSER...")
        await browser.close()
        process.abort()
    }
}


async function extraChecking(page , email , password, browser,jobid){
    Promise.allSettled([tryLogin(page ,email ,password),captchaFrame(page,email),challengeHeading(page,email,browser,jobid),ContinueButton(page,email),startOver(page,email,browser),arkoseIframe(page,email,browser,jobid)]).then(result => { console.log(result)} ).catch(e=> { console.log("Something Wrong"+e) })
}


async function ifAvailable(page, xpath){
    try{
        await page.waitForSelector(xpath)
        return true
    } catch(e){
        return false
    }
}


YahooLogin(email,password,proxy,port,longitude,latitude,jobid)