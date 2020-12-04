import {Grid, Link, Typography, Box} from "@material-ui/core";
import React, {useState, useContext, useEffect} from "react";
import axios from "axios";
import Navibar from "../component/Navibar";
import Description from "../component/Description";
import InputUrl from "../component/InputUrl";
import Result from "../component/Result";
import Usage from "../component/Usage";
import YobaContext from "../context/YobaContext"
import cookie from 'react-cookies';

function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {"Copyright © "}
            <Link color="inherit" href="#">
                Yoba
            </Link>{" "}
            {new Date().getFullYear()}
            {"."}
        </Typography>
    );
}

const MainPage = () => {
    const [login, toggleLogin] = useState(false);
    const [input, toggleInput] = useState(false);

    // const temp = localStorage.getItem("loginStorage");
    const temp = cookie.load('data');
    const {actions} = useContext(YobaContext);

    useEffect(() => {
        const temp = cookie.load('data');
        if(temp !== undefined){
            actions.setEmail(temp.email);
            actions.setName(temp.name);
        }
    });

    const test = () => {
        try {
            axios
                .get("http://localhost:8000/api/login", {
                    headers: {"Content-Type": "multipart/form-data"},
                    params: {
                        email: temp.email,
                        uuid: temp.uuid,
                    },
                })
                .then((response) => {
                    const data = response.data;
                    // console.log(data);
                    // localStorage.setItem("loginStorage", JSON.stringify(data));
                    cookie.save('data', JSON.stringify(data), {path: '/'});
                    actions.setEmail(temp.email);
                    actions.setName(temp.name);
                    toggleLogin(true);
                })
                .catch(function (error) {
                    if (error.response.status === 401) {
                        // localStorage.removeItem("loginStorage");
                        cookie.remove('data');
                        toggleLogin(false);
                        toggleInput(false);
                        alert("please, you need sign in again.");
                    }
                });
        } catch (e) {

            console.log(e);
        }
    };

    return (
        <div onLoad={test}>
            <Navibar
                login={login}
                toggleInput={toggleInput}
                toggleLogin={toggleLogin}
            />

            <Grid>
                <Description/>
            </Grid>

            {login ? (
                <InputUrl
                    toggleInput={toggleInput}
                    toggleLogin={toggleLogin}
                    input={input}
                ></InputUrl>
            ) : (
                <></>
            )}

            {input & login ? (
                <Result></Result>
            ) : (
                <></>
            )}
            <Grid>
                <Usage/>
            </Grid>

            <Box mt={8}>
                <Copyright/>
            </Box>
        </div>
    );
};

export default MainPage;
