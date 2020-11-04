import React, {createContext, useState} from 'react'

const YobaContext = createContext({
    state: { url : "", },
    actions: {
        setUrl: () => {},
    }
})

const YobaProvidor = ({children}) => {
    const [url, setUrl] = useState();

    const value = {
        states: {url,},
        actions: {setUrl,}
    };

    return (
        <YobaContext.Provider value={value}>{children}</YobaContext.Provider>
    )
};

const {Consumer: YobaConsumer} = YobaContext;

export {YobaProvidor, YobaConsumer};

export default YobaContext;