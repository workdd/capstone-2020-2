import React, {createContext, useState} from 'react'

const YobaContext = createContext({
    state: { url : "", platform : "", videoid : "", email : "", name : "",},
    actions: {
        setUrl: () => {},
        setPlatform: () => {},
        setVideoid: () => {},
        setEmail: () => {},
        setName: () => {},
    }
})

const YobaProvidor = ({children}) => {
    const [url, setUrl] = useState();
    const [platform, setPlatform] = useState();
    const [videoid, setVideoid] = useState();
    const [email, setEmail] = useState();
    const [name, setName] = useState();

    const value = {
        states: {url, platform, videoid, email, name},
        actions: {setUrl, setPlatform, setVideoid, setEmail, setName}
    };

    return (
        <YobaContext.Provider value={value}>{children}</YobaContext.Provider>
    )
};

const {Consumer: YobaConsumer} = YobaContext;

export {YobaProvidor, YobaConsumer};

export default YobaContext;