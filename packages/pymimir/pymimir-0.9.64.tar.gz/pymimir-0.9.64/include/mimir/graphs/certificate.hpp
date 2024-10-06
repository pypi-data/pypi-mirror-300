/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef MIMIR_GRAPHS_CERTIFICATE_HPP_
#define MIMIR_GRAPHS_CERTIFICATE_HPP_

#include "mimir/common/hash.hpp"
#include "mimir/graphs/declarations.hpp"

#include <memory>
#include <string>
#include <vector>

namespace mimir
{
class Certificate
{
private:
    size_t m_num_vertices;
    size_t m_num_edges;
    std::string m_nauty_certificate;
    ColorList m_canonical_initial_coloring;

public:
    Certificate(size_t num_vertices, size_t num_edges, std::string nauty_certificate, ColorList canonical_initial_coloring);

    bool operator==(const Certificate& other) const;

    size_t get_num_vertices() const;
    size_t get_num_edges() const;
    const std::string& get_nauty_certificate() const;
    const ColorList& get_canonical_initial_coloring() const;
};

struct UniqueCertificateSharedPtrHash
{
    size_t operator()(const std::shared_ptr<const Certificate>& element) const;
};

struct UniqueCertificateSharedPtrEqualTo
{
    size_t operator()(const std::shared_ptr<const Certificate>& lhs, const std::shared_ptr<const Certificate>& rhs) const;
};
}

template<>
struct std::hash<mimir::Certificate>
{
    size_t operator()(const mimir::Certificate& element) const;
};

#endif