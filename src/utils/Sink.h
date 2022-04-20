#ifndef CURAENGINE_SINK_H
#define CURAENGINE_SINK_H

#include <iostream>
#include <mutex>
#include <spdlog/details/null_mutex.h>
#include <spdlog/sinks/base_sink.h>

#include "utils/Concepts.h"

namespace cura::logger::sinks
{
template<typename Mutex>
class VtkSync : public spdlog::sinks::base_sink<Mutex>
{
  public:
    void log(concepts::Poly auto poly)
    {
        sink_it_(poly);
    }

  protected:
    void sink_it_(concepts::Poly auto poly)
    {
        std::cout << "you got poly" << std::endl;
    }

    void sink_it_(const spdlog::details::log_msg& msg) override
    {
        spdlog::memory_buf_t formatted;
        spdlog::sinks::base_sink<Mutex>::formatter_->format(msg, formatted);
        std::cout << fmt::to_string(formatted);
    }

    void flush_() override
    {
        std::cout << std::flush;
    }
};

using vtk_sync_mt = VtkSync<std::mutex>;
using vtk_sync_st = VtkSync<spdlog::details::null_mutex>;
} // namespace cura::logger::sinks
#endif // CURAENGINE_SINK_H
