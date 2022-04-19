#ifndef CURAENGINE_FORMAT_H
#define CURAENGINE_FORMAT_H

#include <fmt/core.h>
#include <fmt/format.h>
#include <fmt/ranges.h>
#include <ranges>

#include "utils/IntPoint.h"
#include "utils/polygon.h"

template<>
struct fmt::formatter<cura::Point>
{
    char presentation = 'a';

    constexpr auto parse(format_parse_context& ctx) -> decltype(ctx.begin())
    {
        auto it = ctx.begin();
        auto end = ctx.end();
        if (it != end && (*it == 'a' || *it == 'i'))
        {
            presentation = *it++;
        }

        if (it != end && *it != '}')
        {
            throw format_error("invalid format");
        }

        return it;
    }
    template<typename FormatContext>
    auto format(cura::Point p, FormatContext& ctx) -> decltype(ctx.out())
    {
        return presentation == 'a' ? format_to(ctx.out(), "[{}, {}]", p.X, p.Y) : format_to(ctx.out(), "{}, {}", p.X, p.Y);
    }
};

template<>
struct fmt::formatter<cura::Polygon>
{
    char presentation = 'a';

    constexpr auto parse(format_parse_context& ctx) -> decltype(ctx.begin())
    {
        auto it = ctx.begin();
        auto end = ctx.end();
        if (it != end && (*it == 'a' || *it == 'i'))
        {
            presentation = *it++;
        }

        if (it != end && *it != '}')
        {
            throw format_error("invalid format");
        }

        return it;
    }
    template<typename FormatContext>
    auto format(auto p, FormatContext& ctx) -> decltype(ctx.out())
    {
        return presentation == 'a' ? format_to(ctx.out(), "[{}]", fmt::join(p.begin(), p.end(), ", ")) :  format_to(ctx.out(), "{}", fmt::join(p.begin(), p.end(), ", "));
    }
};

template<>
struct fmt::formatter<cura::Polygons>
{
    char presentation = 'a';

    constexpr auto parse(format_parse_context& ctx) -> decltype(ctx.begin())
    {
        auto it = ctx.begin();
        auto end = ctx.end();
        if (it != end && (*it == 'a' || *it == 'i'))
        {
            presentation = *it++;
        }

        if (it != end && *it != '}')
        {
            throw format_error("invalid format");
        }

        return it;
    }
    template<typename FormatContext>
    auto format(auto p, FormatContext& ctx) -> decltype(ctx.out())
    {
        return presentation == 'a' ? format_to(ctx.out(), "[{}]", fmt::join(p.begin(), p.end(), ", ")) :  format_to(ctx.out(), "{}", fmt::join(p.begin(), p.end(), ", "));
    }
};

#endif // CURAENGINE_FORMAT_H
