import React, {createContext, useState} from 'react'

const YobaContext = createContext({
    state: { url : "", platform : "", videoid : ""},
    actions: {
        setUrl: () => {},
        setPlatform: () => {},
        setVideoid: () => {},
    }
})

const YobaProvidor = ({children}) => {
    const [url, setUrl] = useState();
    const [platform, setPlatform] = useState();
    const [videoid, setVideoid] = useState();

    const value = {
        states: {url, platform, videoid},
        actions: {setUrl, setPlatform, setVideoid}
    };

    return (
        <YobaContext.Provider value={value}>{children}</YobaContext.Provider>
    )
};

const {Consumer: YobaConsumer} = YobaContext;

export {YobaProvidor, YobaConsumer};

export default YobaContext;