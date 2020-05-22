// ======================
// BoggleController class definition
// ======================
class BoggleController {
    constructor(timer) {
        this.timer = timer + 1;
        this.score = 0;
        this.guesses = new Array();
    }

    /**
     * Check guess to see if it is a valid word in our Boggle
     * board and hasn't been guessed already
     * @param {String} arg1 The guessed word that should be checked
     */
    async checkGuess(guess) {
        if (this.guesses.includes(guess)) {
            return "Already guessed that word!"
        }
        else {
            let response;
            try {
                response = await axios.post("/guess", {"guess": guess});
            } 
            catch(err) {
                alert("Server returned an error. Wait a few moments and restart your game.");
                return;
            }
            return this.updateScore(guess, response.data.result);
        }
        
        
    }

    /**
     * Update the game's score if the result returned from the API is ok
     * @param {String} guess  The guessed word
     * @param {String} result String that is returned from the API call to guess
     */
    updateScore(guess, result) {
        if (result === 'ok') {
            this.score += guess.length;
            this.guesses.push(guess);
            return `Good guess! +${guess.length} points`;
        } else if (result === 'not-word'){
            return `${guess} is not a word!`;
        } else if (result === 'not-on-board') {
            return 'That word is not on the board!';
        } else {
            return "unexpected response from API";
        }
    }

    /**
     * Simple helper method to send the current score to the API
     */
    sendScoreToServer() {
        let response;
        try {
            response = axios.post('/send-score', {"score": this.score});
        }
        catch(err){
            console.log(`Score was not sent to server. Error msg: ${err}`);
        }
    }
}

// ======================
// Game flow
// ======================
const submitBtn = $('#submitBtn');
const guessText = $('#guessText');
const scoreboard = $('#scoreboard');
const scoreboardMsg = $('#scoreboard-msg');
const timerMsg = $('#timer-msg');

let controller = new BoggleController(60);

submitBtn.on("click", handleSubmit);
scoreboard.text(controller.score);

async function handleSubmit(e) {
    e.preventDefault();
    guess_result = await controller.checkGuess(guessText.val());
    scoreboardMsg.text(guess_result);
    scoreboard.text(controller.score);
    guessText.val(""); // clear out the text input
}

let timerInterval = setInterval(() => {
    if (controller.timer === 0) {
        clearInterval(timerInterval);
        controller.sendScoreToServer();
        guessText.attr('readonly', true);
        submitBtn.attr('disabled', true);
        scoreboardMsg.text("Time is up! Good job!");
    } else {
        controller.timer--;
        timerMsg.text(controller.timer);
    }
}, 1000)



