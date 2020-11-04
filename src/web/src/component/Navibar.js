import {AppBar, Grid, Typography} from "@material-ui/core";
import React, {useContext, useEffect} from "react";
import YobaLogo from "../yoba_logo.png";
import Login from "./Login.js"
import YobaContext from "../context/YobaContext"
import cookie from 'react-cookies'

const NaviBar = (props) => {
    const {actions, states} = useContext(YobaContext);

    useEffect(() => {
        const temp = cookie.load('data');
        if(temp !== undefined){
            actions.setEmail(temp.email);
            actions.setName(temp.name);
            props.toggleLogin(true);
        }
    });

    const logout = () => {
        cookie.remove('data');
        if (props.login === true) {
            // localStorage.removeItem("loginStorage");

            props.toggleLogin(false);
            props.toggleInput(false);
            alert("sign out");
        } else {
            alert("Please, sign in from the bottom page.");
        }
    };
    const onClick = () => {
        if (props.login === true) {
            alert("welcome");
        }
    };

    return (
        <AppBar position="sticky" color="default">
            <Grid
                container
                alignItems="center"
                direction="row"
                justify="center"
                style={{paddingTop: 3, paddingBottom: 3}}
            >
                <Grid xs={1}>
                    <Typography
                        variant="h6"
                        style={{
                            textTransform: "none",
                            color: "black",
                            marginLeft: 20,
                            marginRight: 20,
                        }}
                    >
                        YOBA
                    </Typography>
                </Grid>
                <Grid xs={2}></Grid>

                <Grid xs={6}>
                    <img alt="logo" src={YobaLogo} height="70px"/>
                </Grid>

                <Grid xs={2}>
                    <Typography
                        variant="h6"
                        style={{
                            textTransform: "none",
                            color: "black",
                            marginLeft: 20,
                            marginRight: 30,
                        }}
                        onClick={onClick}
                    >
                        {props.login ? "Welcome! " + states.name : ""}
                    </Typography>
                </Grid>
                <Grid xs={1}>
                    {props.login ? (
                        <Typography
                            variant="h6"
                            style={{
                                textTransform: "none",
                                color: "black",
                                marginLeft: 20,
                                marginRight: 30,
                            }}
                            onClick={logout}
                        >
                            Sign out
                        </Typography>
                    ) : (
                        <Login toggleLogin={props.toggleLogin}></Login>
                    )}
                </Grid>
            </Grid>
        </AppBar>
    );
};

export default NaviBar;
