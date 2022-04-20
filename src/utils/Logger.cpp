#include <memory>

#include "utils/Logger.h"
#include "utils/Sink.h"

#include <spdlog/spdlog.h>
#include <spdlog/async.h>
#include <spdlog/async_logger.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/details/os.h>
#include <spdlog/cfg/helpers.h>

namespace cura::logger
{

void init()
{
    auto log_file = spdlog::details::os::getenv("CURAENGINE_LOGFILE");
    if (log_file.empty())
    {
        log_file = "/mnt/projects/ultimaker/cura/curaengine/curaengine.log";
    }
    auto async_file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(log_file);
    auto async_vtk = std::make_shared<logger::sinks::vtk_sync_mt>();
    spdlog::init_thread_pool(8192, 1); // Queue with 8192 items and 1 backing thread

    auto logger = spdlog::stdout_color_mt<spdlog::async_factory>("default");
    logger->sinks().push_back(async_file_sink);
    logger->set_level(spdlog::level::info);

    auto support = spdlog::stdout_color_mt<spdlog::async_factory>("support");
    support->sinks().push_back(async_file_sink);
    support->set_level(spdlog::level::warn);

    auto fffpolygongenerator =spdlog::stdout_color_mt<spdlog::async_factory>("fffpolygongenerator");
    fffpolygongenerator->sinks().push_back(async_file_sink);
    fffpolygongenerator->set_level(spdlog::level::warn);

    auto fffprocessor = spdlog::stdout_color_mt<spdlog::async_factory>("fffprocessor");
    fffprocessor->sinks().push_back(async_file_sink);
    fffprocessor->set_level(spdlog::level::warn);

    auto gcodeexport = spdlog::stdout_color_mt<spdlog::async_factory>("gcodeexport");
    gcodeexport->sinks().push_back(async_file_sink);
    gcodeexport->set_level(spdlog::level::warn);

//    auto vtk = spdlog::create_async<logger::sinks::vtk_sync_mt>("vtk");
    auto vtk = std::make_shared<logger::cura_logger>("vtk");
    vtk->sinks().push_back(async_vtk);
    vtk->set_level(spdlog::level::debug);
    spdlog::register_logger(vtk);

    spdlog::set_default_logger(logger);

    // Set log levels using the environment variable CURAENGINE_LOG_LEVEL
    // set global level to debug: CURAENGINE_LOG_LEVEL="debug"
    // turn of all except support: CURAENGINE_LOG_LEVEL="off,support=debug"
    // set global to warn except support: CURAENGINE_LOG_LEVEL="warn,support=debug"
    auto env_val = spdlog::details::os::getenv("CURAENGINE_LOG_LEVEL");
    if (!env_val.empty())
    {
        spdlog::info(env_val);
        spdlog::cfg::helpers::load_levels(env_val);
    }
}


} // namespace cura::logger
