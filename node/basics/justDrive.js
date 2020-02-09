const EasyGopigo3 = require('node-gopigo3').EasyGopigo3,
    gpg = new EasyGopigo3(),
    sleep = require('sleep');

/**
 * const Gopigo3 = require('node-gopigo3').Gopigo3
 * const gpg = new EasyGopigo3();
 *
 * What is the difference between EasyGopigo3 and Gopigo3?
 */

/*
console.log('Press any key to exit');

process.stdin.setRawMode(true);
process.stdin.resume();
process.stdin.on('data', () => {
    gpg.stop();
    gpg.resetAll();
    process.exit(0);
});
*/

gpg.driveCm(50, () => {
    console.log('Wait 1 second.');
    sleep.sleep(1);

    console.log('Turn right 1 second.');
    gpg.right();
    sleep.sleep(1);

    console.log('Turn left 1 second.');
    gpg.left();
    sleep.sleep(1);

    console.log('Stop!');
    gpg.stop();

    console.log('Done!');
});
