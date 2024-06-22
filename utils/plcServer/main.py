if __name__=="__main__":
    from HslCommunication import SiemensS7Net, SiemensPLCS
    from snap7.util import get_int, get_real, get_dword, get_string, get_byte, get_word, get_bool
    from fastapi import FastAPI
    import uvicorn
    from server import app, connect_plc
    import config

    if config.plcForwarderUrl:
        connect_plc(config.plcForwarderUrl, config.plcForwarderRack, config.plcForwarderSlot)
    uvicorn.run(app=app, host=config.server_ip, port=config.server_port)
