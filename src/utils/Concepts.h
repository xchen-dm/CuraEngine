#ifndef CURAENGINE_CONCEPTS_H
#define CURAENGINE_CONCEPTS_H

#include <concepts>
#include <type_traits>
#include <ranges>

namespace cura::concepts
{
template<class T>
concept Number = std::integral<T> || std::floating_point<T>;

template<class T>
concept Point = requires(T p)
{
    { p.X } -> Number;
    { p.Y } -> Number;
};

template<class T>
concept Poly = std::ranges::range<T>;

} // namespace cura


#endif // CURAENGINE_CONCEPTS_H
