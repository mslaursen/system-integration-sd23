import express from 'express';

const app = express();

app.use(express.static('public'));

const randomNumbers = [];

app.get("/randomNumbers", (req, res) => {
    res.send({data: randomNumbers});
});

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

app.get("/simulateNewRandomNumbers", (req, res) => {
    const newNumber = getRandomInt(3, 1001);
    randomNumbers.push(newNumber);
    res.send({data: randomNumbers});
}
);


const PORT = 8081;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));



