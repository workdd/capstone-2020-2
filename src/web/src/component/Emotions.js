import React, {useEffect, useState, useContext} from "react";
import axios from "axios";
import {Line} from "react-chartjs-2";
import {MDBContainer} from "mdbreact";
import CircularProgress from "@material-ui/core/CircularProgress";
import YobaContext from "../context/YobaContext";

function humanReadable(seconds) {
    var pad = function (x) {
        return x < 10 ? "0" + x : x;
    };
    return (
        pad(parseInt(seconds / (60 * 60))) +
        ":" +
        pad(parseInt((seconds / 60) % 60)) +
        ":" +
        pad(seconds % 60)
    );
}

const Emotions = (props) => {
    const { states } = useContext(YobaContext)

    let state = {
        dataLine: {
            labels: [],
            datasets: [
                {
                    label: "joy",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(225, 204,230, .3)",
                    borderColor: "rgb(205, 130, 158)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(205, 130, 158)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
                {
                    label: "love",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(184, 185, 210, .3)",
                    borderColor: "rgb(35, 26, 136)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(35, 26, 136)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
                {
                    label: "angry",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(184, 185, 210, .3)",
                    borderColor: "rgb(135, 26, 136)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(135, 26, 136)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
                {
                    label: "neutral",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(184, 185, 210, .3)",
                    borderColor: "rgb(135, 126, 36)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(135, 126, 36)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
                {
                    label: "sadness",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(184, 185, 210, .3)",
                    borderColor: "rgb(35, 76, 36)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(35, 76, 36)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
                {
                    label: "fear",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(184, 185, 210, .3)",
                    borderColor: "rgb(35, 76, 116)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(35, 76, 116)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
                {
                    label: "surprise",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(184, 185, 210, .3)",
                    borderColor: "rgb(135, 176, 116)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgb(135, 176, 116)",
                    pointBackgroundColor: "rgb(255, 255, 255)",
                    pointBorderWidth: 10,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgb(0, 0, 0)",
                    pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                },
            ],
        },
    };
    const [test, setTest] = useState({
        labels: [],
        datasets: [
            {
                label: "joy",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(225, 204,230, .3)",
                borderColor: "rgb(205, 130, 158)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(205, 130, 158)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
            {
                label: "love",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(35, 26, 136)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(35, 26, 136)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
            {
                label: "angry",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(135, 26, 136)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(135, 26, 136)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
            {
                label: "neutral",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(135, 126, 36)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(135, 126, 36)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
            {
                label: "sadness",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(35, 76, 36)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(35, 76, 36)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
            {
                label: "fear",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(35, 76, 116)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(35, 76, 116)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
            {
                label: "surprise",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(135, 176, 116)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(135, 176, 116)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
            },
        ],
    });

    const [load, setLoad] = useState(false);
    const [bin, setBin] = useState();
    const [realtime, setRealtime] = useState("00:00:00");

    const onlyClick = (e) => {
        if (e.length > 0) {
            setRealtime(humanReadable(e[0]._index * bin));
        }
    };

    useEffect(() => {
        try {
            axios
                .get("http://localhost:8000/api/predict7", {
                    headers: {"Content-Type": "multipart/form-data"},
                    params: {
                        url: states.url,
                    },
                })
                .then((response) => {
                    const data = response.data;
                    let datasets = state.dataLine.datasets;

                    for (var i = 0; i < 100; i++) {
                        state.dataLine.labels = state.dataLine.labels.concat(i);
                        for (let emo = 0; emo < datasets.length; emo++) {
                            state.dataLine.datasets[emo].data = state.dataLine.datasets[emo].data.concat(
                                data.predict[datasets[0].label][i]
                            );
                        }
                    }
                    for (i = 99; i > 0; i--) {

                        let isEmpty = true;
                        for (let emoidx = 0; emoidx < datasets.length; emoidx++) {
                            if (state.dataLine.datasets[emoidx].data[i] !== 0) {
                                isEmpty = false;
                                break;
                            }
                        }

                        if (isEmpty) {
                            state.dataLine.labels.splice(i, 1);

                            for (let emo = 0; emo < datasets.length; emo++) {
                                state.dataLine.datasets[emo].data.splice(i, 1);
                            }
                        } else {
                            break;
                        }
                    }
                    setTest(state.dataLine);
                    setBin(data.bin);
                    setLoad(true);
                })
                .catch();
        } catch (e) {
            console.log(e);
        }
    }, [states]);

    return (
        <MDBContainer>
            <h3 className="mt-5">Emotions Sentiment</h3>
            {load ? (
                <div style={{height: 580}}>
                    <Line
                        data={test}
                        options={{responsive: true}}
                        onElementsClick={(e) => {
                            onlyClick(e);
                        }}
                    />
                    <sub>chats / {bin} sec</sub>
                    <br></br>
                    position is {realtime}
                </div>
            ) : (
                <div style={{height: 580}}>
                    <CircularProgress color="secondary"/>
                </div>
            )}
        </MDBContainer>
    );
};

export default Emotions;
