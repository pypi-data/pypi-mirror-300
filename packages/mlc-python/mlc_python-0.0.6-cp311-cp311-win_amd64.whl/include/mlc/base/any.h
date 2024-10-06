#ifndef MLC_BASE_ANY_H_
#define MLC_BASE_ANY_H_
#include "./utils.h"
#include <cstring>
#include <utility>

namespace mlc {
struct AnyView : public MLCAny {
public:
  friend struct ::mlc::Any;
  /***** Section 1. Default constructor/destructors *****/
  MLC_INLINE ~AnyView() = default;
  MLC_INLINE AnyView() : MLCAny() {}
  MLC_INLINE AnyView(std::nullptr_t) : MLCAny() {}
  MLC_INLINE AnyView(NullType) : MLCAny() {}
  MLC_INLINE AnyView &operator=(std::nullptr_t) { return this->Reset(); }
  MLC_INLINE AnyView &operator=(NullType) { return this->Reset(); }
  MLC_INLINE AnyView &Reset() {
    *(static_cast<MLCAny *>(this)) = MLCAny();
    return *this;
  }
  /***** Section 2. Conversion between Any/AnyView *****/
  MLC_INLINE AnyView(const AnyView &src) = default;
  MLC_INLINE AnyView(AnyView &&src) = default;
  MLC_INLINE AnyView(const Any &src);
  MLC_INLINE AnyView(Any &&src);
  MLC_INLINE AnyView &operator=(const AnyView &src) = default;
  MLC_INLINE AnyView &operator=(AnyView &&src) = default;
  MLC_INLINE AnyView &operator=(const Any &src);
  MLC_INLINE AnyView &operator=(Any &&src);
  /***** Section 3. Conversion between POD and object pointers *****/
  template <typename T> MLC_INLINE_NO_MSVC T Cast() const;
  template <typename T> MLC_INLINE_NO_MSVC T CastWithStorage(Any *storage) const;
  template <typename T> MLC_INLINE operator T() const { return this->Cast<T>(); }
  template <typename T> MLC_INLINE AnyView(const T &src);
  template <typename T> MLC_INLINE AnyView &operator=(const T &src) {
    AnyView(src).Swap(*this);
    return *this;
  }
  /***** Misc *****/
  Str str() const;
  friend std::ostream &operator<<(std::ostream &os, const AnyView &src);

protected:
  MLC_INLINE void Swap(MLCAny &src) {
    MLCAny tmp = *this;
    *static_cast<MLCAny *>(this) = src;
    src = tmp;
  }
};

struct Any : public MLCAny {
  friend struct ::mlc::AnyView;
  /***** Section 1. Default constructor/destructors *****/
  MLC_INLINE ~Any() { this->Reset(); }
  MLC_INLINE Any() : MLCAny() {}
  MLC_INLINE Any(std::nullptr_t) : MLCAny() {}
  MLC_INLINE Any(NullType) : MLCAny() {}
  MLC_INLINE Any &operator=(std::nullptr_t) { return this->Reset(); }
  MLC_INLINE Any &operator=(NullType) { return this->Reset(); }
  MLC_INLINE Any &Reset() {
    this->DecRef();
    *(static_cast<MLCAny *>(this)) = MLCAny();
    return *this;
  }
  /***** Section 2. Conversion between Any/AnyView *****/
  MLC_INLINE Any(const Any &src);
  MLC_INLINE Any(Any &&src);
  MLC_INLINE Any(const AnyView &src);
  MLC_INLINE Any(AnyView &&src);
  MLC_INLINE Any &operator=(const Any &src);
  MLC_INLINE Any &operator=(Any &&src);
  MLC_INLINE Any &operator=(const AnyView &src);
  MLC_INLINE Any &operator=(AnyView &&src);
  /***** Section 3. Conversion between POD and object pointers *****/
  template <typename T> MLC_INLINE_NO_MSVC T Cast() const;
  template <typename T> MLC_INLINE_NO_MSVC T CastWithStorage(Any *storage) const;
  template <typename T> MLC_INLINE operator T() const { return this->Cast<T>(); }
  template <typename T> MLC_INLINE Any(const T &src);
  template <typename T> MLC_INLINE Any &operator=(const T &src) {
    Any(src).Swap(*this);
    return *this;
  }
  /***** Misc *****/
  Str str() const;
  friend std::ostream &operator<<(std::ostream &os, const Any &src);

protected:
  MLC_INLINE void Swap(MLCAny &src) {
    MLCAny tmp = *this;
    *static_cast<MLCAny *>(this) = src;
    src = tmp;
  }
  MLC_INLINE void IncRef() {
    if (!::mlc::base::IsTypeIndexPOD(this->type_index)) {
      ::mlc::base::IncRef(this->v_obj);
    }
  }
  MLC_INLINE void DecRef() {
    if (!::mlc::base::IsTypeIndexPOD(this->type_index)) {
      ::mlc::base::DecRef(this->v_obj);
    }
  }
  MLC_INLINE void SwitchFromRawStr() {
    if (this->type_index == static_cast<int32_t>(MLCTypeIndex::kMLCRawStr)) {
      this->type_index = static_cast<int32_t>(MLCTypeIndex::kMLCStr);
      this->v_obj =
          reinterpret_cast<MLCObject *>(::mlc::base::StrCopyFromCharArray(this->v_str, std::strlen(this->v_str)));
    }
  }
};

template <std::size_t N> struct AnyViewArray {
  template <typename... Args> void Fill(Args &&...args);
  AnyView v[N];
};

template <> struct AnyViewArray<0> {
  template <typename... Args> void Fill(Args &&...args);
  AnyView *v = nullptr;
};
} // namespace mlc

namespace mlc {
namespace base {
template <typename... Args> struct AnyViewArrayFill {
  template <std::size_t i, typename Arg> MLC_INLINE static void Apply(AnyView *v, Arg &&arg) {
    v[i] = AnyView(std::forward<Arg>(arg));
  }
  template <std::size_t... I> MLC_INLINE static void Run(AnyView *v, Args &&...args, std::index_sequence<I...>) {
    using TExpander = int[];
    (void)TExpander{0, (Apply<I>(v, std::forward<Args>(args)), 0)...};
  }
};
} // namespace base
} // namespace mlc

#endif // MLC_BASE_ANY_H_
