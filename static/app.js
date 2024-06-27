class BoggleGame {
    constructor(boardId, secs = 60) {
        this.secs = secs; // game length
        this.showTimer();

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        // every 1000 msec, "tick"
        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".add-word").on("submit", this.handleSubmit.bind(this));
    }

    // Append a word to the list of found words
    showWord(word) {
        $("<li>")
            .text(word)
            .addClass('appended-word') // Add class to the <li> element
            .appendTo(".words");       // Append <li> to the .words container
    }

    // Update the score in the DOM
    showScore() {
        $(".score").text(this.score);
    }

    // Display a status message
    showMessage(msg, cls) {
        $(".msg")
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    // Handle form submission for word guess
    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word");

        let word = $word.val().trim();
        if (!word) return;

        // Check if word has already been found
        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "warning");
            $word.val('')
            return;
        }

        // Send word to server for validation
        const response = await axios.get("/check-word", { params: { word: word } });
        const result = response.data.result;

        // Display appropriate message based on server response
        if (result === "not-word") {
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if (result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
            // Valid word: update score, list of words, and message
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }

        // Clear input field and focus
        $word.val("").focus();
    }

    // Update timer display
    showTimer() {
        $(".timer").text(this.secs);
    }

    // Countdown timer logic
    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.endGame();
        }
    }

    // End game: send score to server and update message
    async endGame() {
        // hide the input from user to disable entering more words
        $(".add-word").hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}

// Initialize the Boggle game when the document is ready
$(document).ready(function () {
    new BoggleGame("board");
});
