import {Grid, Typography} from "@material-ui/core";
import React from "react";
import {makeStyles} from "@material-ui/core/styles";
import ViewerReact from "./ViewerReact";

const login = require("../flaticon/login.png");
const url = require("../flaticon/url.png");
const analysis = require("../flaticon/analysis.png");
const edit = require("../flaticon/edit.png");
const login_description = require("../flaticon/login-description.png");
const url_description = require("../flaticon/url-description.png");
const analysis_description = require("../flaticon/analysis-description.png");
const edit_description = require("../flaticon/edit-description.png");

const next = require("../flaticon/next.png");

const images = [
    login,
    url,
    analysis,
    edit
]

const descriptions = [
  login_description,
  url_description,
  analysis_description,
  edit_description
];

const img_style = {width: 128, height: 128};
const arrow_style = {width: 64, height: 64, marginLeft: 20, marginRight: 20};
const img_info_style = {
  width: 192,
  height: 192,
  marginLeft: 20,
  marginRight: 20,
};

const useStyles = makeStyles((theme) => ({
  root: {
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    height: 200,
    width: "100%",
    background: "#E2E2E2"
  },
}));

const Usage = () => {
  const classes = useStyles();

  return (
      <div>
        <div style={{height: "40px"}}></div>
        <Grid container className={classes.root} spacing={3}>
            {images.map((image, idx) =>{
                return (
                    <div>
                        <img src={image} style={img_info_style}/>
                        {idx !== images.length - 1 ? (
                            <img src={next} style={arrow_style}/>
                        ) : (
                                <></>
                            )}
                        }
                    </div>
            )
            })}
        </Grid>
        <Grid container className={classes.root} spacing={3}>
          {descriptions.map((description, idx) => <img src={description} style={img_info_style}/>)}
        </Grid>
      </div>
  );
};

export default Usage;
