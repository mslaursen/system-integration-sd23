console.log(new Date().toString());

const date = new Date();

// ISO 8601

const danishDate = new Intl.DateTimeFormat("da-dk").format(date);
console.log(danishDate);

const americanDate = new Intl.DateTimeFormat("en-us").format(date);
console.log(americanDate);