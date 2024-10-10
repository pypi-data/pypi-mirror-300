#include "one_of.h"

#include "../../generator_data.h"


namespace dlplan::generator::rules {
void OneOfConcept::generate_impl(const core::States& states, int target_complexity, GeneratorData& data, core::DenotationsCaches& caches) {
    core::SyntacticElementFactory& factory = data.m_factory;
    assert(target_complexity == 1);
    for (const auto& constant : factory.get_vocabulary_info()->get_constants()) {
        auto element = factory.make_one_of_concept(constant);
        auto denotations = element->evaluate(states, caches);
        if (data.m_concept_hash_table.insert(denotations).second) {
            std::get<2>(data.m_generated_features).push_back(element);
            data.m_concepts_by_iteration[target_complexity].push_back(std::move(element));
            increment_generated();
        }
    }
}

std::string OneOfConcept::get_name() const {
    return "c_one_of";
}

}
