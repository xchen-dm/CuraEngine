#ifndef CURAENGINE_LOGGER_H
#define CURAENGINE_LOGGER_H

#include <string>
#include <utility>
#include <ranges>

#include <spdlog/logger.h>

#include "utils/Concepts.h"
#include "utils/Format.h"
#include <utils/polygon.h>
#include "utils/Sink.h"

namespace cura::logger
{
void init();

class SPDLOG_API cura_logger : public spdlog::logger
{
  public:
    explicit cura_logger(std::string name) : spdlog::logger(std::move(name)) {}

    void log(spdlog::level::level_enum lvl, cura::Polygons poly)
    {
        bool log_enabled = should_log(lvl);
        bool traceback_enabled = tracer_.enabled();
        if (!log_enabled && !traceback_enabled)
        {
            return;
        }

        log_it_(poly, log_enabled, traceback_enabled);
    }

  protected:
    void sink_it_(concepts::Poly auto poly)
      {
          std::ranges::for_each(sinks_, [poly](auto s){
                std::reinterpret_pointer_cast<sinks::vtk_sync_mt>(s)->log(poly); });
      };

    void log_it_(concepts::Poly auto poly, bool log_enabled, bool traceback_enabled)
    {
        if (log_enabled)
        {
            sink_it_(poly);
        }
    }

};


}

#endif // CURAENGINE_LOGGER_H
