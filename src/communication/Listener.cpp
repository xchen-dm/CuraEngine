//Copyright (c) 2018 Ultimaker B.V.
//CuraEngine is released under the terms of the AGPLv3 or higher.

#ifdef ARCUS

#include <Arcus/Error.h> //To process error codes.

#include "Listener.h"
#include <spdlog/spdlog.h>

namespace cura
{

void Listener::stateChanged(Arcus::SocketState)
{
    //Do nothing.
}

void Listener::messageReceived()
{
    //Do nothing.
}

void Listener::error(const Arcus::Error& error)
{
    if (error.getErrorCode() == Arcus::ErrorCode::Debug)
    {
        spdlog::get("console")->debug(error.getErrorMessage().c_str());
    }
    else
    {
        spdlog::get("console")->error(error.getErrorMessage().c_str());
    }
}

} //namespace cura

#endif //ARCUS